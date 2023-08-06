"""utilities to handle waylay authentication"""

from datetime import datetime
from functools import lru_cache
from enum import Enum
from dataclasses import dataclass
from typing import (
    Optional, Generator, ClassVar,
    Dict, Any, List, Callable
)
import json
import abc

import base64
import binascii
import httpx
import jwt
import jwt.exceptions as jwt_exc
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm
import Crypto.PublicKey.RSA
from Crypto.PublicKey.pubkey import pubkey

from .exceptions import AuthError

try:
    jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))
except ValueError:
    # already registered
    pass

# http client dependencies
_http = httpx


class CredentialsType(str, Enum):
    """
    Supported Waylay Authentication Methods.
    Note that username/password authentication (as used in our IDP at https://login.waylay.io)
    is not (yet) supported.
    """
    CLIENT = 'client_credentials'
    APPLICATION = 'application_credentials'
    TOKEN = 'token'
    INTERACTIVE = 'interactive'


DEFAULT_ACCOUNTS_URL = 'https://accounts-api.waylay.io'
TokenString = str


class WaylayCredentials(abc.ABC):
    """Base class for the representation of credentials to the waylay platform"""
    accounts_url: str
    credentials_type: ClassVar[CredentialsType] = CredentialsType.INTERACTIVE

    @abc.abstractmethod
    def to_dict(self, obfuscate=True) -> Dict[str, Any]:
        """convert the credentials to a json-serialisable representation"""

    def __repr__(self):
        return f'<{self.__class__.__name__}({str(self)})>'

    def __str__(self):
        return json.dumps(self.to_dict(obfuscate=True))

    @abc.abstractmethod
    def is_well_formed(self) -> bool:
        """
        Validates that these credentials are well-formed.
        This does not assure that they will lead to a succesfull authentication.
        """


@dataclass(repr=False)
class AccountsUrlMixin:
    """data class mixin for the 'accounts_url' property"""
    accounts_url: str = DEFAULT_ACCOUNTS_URL


@dataclass(repr=False, init=False)
class ApiKeySecretMixin(AccountsUrlMixin):
    """data class mixin for the 'api_key' and 'api_secret'"""
    api_key: str = ''
    api_secret: str = ''

    def __init__(self, api_key: str, api_secret: str, accounts_url: str = DEFAULT_ACCOUNTS_URL):
        super().__init__(accounts_url=accounts_url)
        self.api_key = api_key
        self.api_secret = api_secret

    @classmethod
    def create(cls, api_key: str, api_secret: str, accounts_url: str = DEFAULT_ACCOUNTS_URL):
        """create a client credentials object"""
        return cls(api_key=api_key, api_secret=api_secret, accounts_url=accounts_url)

    def to_dict(self, obfuscate=True):
        """convert the credentials to a json-serialisable representation"""
        return dict(
            type=self.credentials_type.value,
            api_key=self.api_key,
            api_secret='********' if obfuscate else self.api_secret,
            accounts_url=self.accounts_url
        )

    def is_well_formed(self) -> bool:
        """
        Validates that these credentials are well-formed.
        This does not assure that they will lead to a succesfull authentication.
        """
        if not (self.api_key and self.api_secret):
            return False
        # api key are 12 bytes hexc encoded
        try:
            if len(bytes.fromhex(self.api_key)) != 12:
                return False
        except ValueError:
            return False
        # api secret are 24 bytes base64 encoded (rfc4648)
        try:
            if len(base64.b64decode(self.api_secret, validate=True)) != 24:
                return False
        except binascii.Error:
            return False
        return True


@dataclass(repr=False, init=False)
class NoCredentials(AccountsUrlMixin, WaylayCredentials):
    """Represents that credentials can be asked interactively when required."""
    credentials_type: ClassVar[CredentialsType] = CredentialsType.INTERACTIVE

    def __init__(self, accounts_url: str = DEFAULT_ACCOUNTS_URL):
        super().__init__(accounts_url=accounts_url)

    def to_dict(self, obfuscate=True):  # pylint: disable=unused-argument
        """convert the credentials to a json-serialisable representation"""
        return dict(
            type=self.credentials_type.value,
            accounts_url=self.accounts_url
        )

    def is_well_formed(self) -> bool:
        return True


@dataclass(repr=False, init=False)
class ClientCredentials(ApiKeySecretMixin, WaylayCredentials):
    """Waylay Credentials: api key and secret of type 'client_credentials'"""
    credentials_type: ClassVar[CredentialsType] = CredentialsType.CLIENT


@dataclass(repr=False, init=False)
class ApplicationCredentials(ApiKeySecretMixin, WaylayCredentials):
    """Waylay Credentials: api key and secret of type 'application_credentials'"""
    credentials_type: ClassVar[CredentialsType] = CredentialsType.APPLICATION
    tenant_id: str = ''


@dataclass(repr=False, init=False)
class TokenCredentials(AccountsUrlMixin, WaylayCredentials):
    """Waylay JWT Token credentials"""
    credentials_type: ClassVar[CredentialsType] = CredentialsType.TOKEN
    token: TokenString = ''

    def __init__(self, token: TokenString, accounts_url: str = DEFAULT_ACCOUNTS_URL):
        super().__init__(accounts_url=accounts_url)
        self.token = token

    def to_dict(self, obfuscate=True):
        return dict(
            type=self.credentials_type.value,
            token='*********' if obfuscate else self.token,
            accounts_url=self.accounts_url
        )

    def is_well_formed(self) -> bool:
        try:
            # WaylayToken constructor decodes the data without signature verification
            return WaylayToken(self.token).tenant is not None
        except AuthError:
            return False


def create_pub_key(entry) -> pubkey:
    """construct an RSA PublicKey from the information published on waylay accounts"""
    if entry['kty'] != 'RSA':
        raise AuthError(f'invalid public key for for{entry["kid"]}')
    modulus = int.from_bytes(base64.b64decode(entry['n']), byteorder='big')
    exponent = int.from_bytes(base64.b64decode(entry['e']), byteorder='big')
    key = Crypto.PublicKey.RSA.construct((modulus, exponent))
    return key


@lru_cache(100)
def fetch_public_key(accounts_url, kid) -> pubkey:
    "cached fetch of public keys for the tenant on waylay accounts"
    jwks_response = _http.get(f"{accounts_url}/jwks")
    jwks_response.raise_for_status()
    for entry in jwks_response.json()['keys']:
        if entry['kid'] == kid:
            return create_pub_key(entry)
    raise AuthError(f'could not find public key for tenant {kid}')


class WaylayToken:
    """Holds a Waylay JWT token"""

    def __init__(self, token_string: str):
        self.token_string = token_string

        try:
            self.token_data = jwt.decode(token_string, verify=False)
        except jwt_exc.PyJWTError as exc:
            raise AuthError(_auth_message_for_exception(exc)) from exc
        except (TypeError, ValueError) as exc:
            raise AuthError(_auth_message_for_exception(exc)) from exc

        self._validated = False

    def validate(self, accounts_url) -> 'WaylayToken':
        """verifies the token signature, essential assertions, and its expiry state"""
        if not self.token_string:
            raise AuthError('no token')

        if not self.token_data:
            raise AuthError('could not parse token data')

        if not self.tenant:
            raise AuthError('invalid token')

        key = fetch_public_key(accounts_url, self.tenant)
        try:
            self.token_data = jwt.decode(
                self.token_string,
                verify=True,
                key=key.exportKey(),  # type: ignore
                algorithms='RS256'
            )
        except jwt_exc.PyJWTError as exc:
            raise AuthError(_auth_message_for_exception(exc)) from exc
        except (TypeError, ValueError) as exc:
            raise AuthError(_auth_message_for_exception(exc)) from exc

        # assert expiry
        if self.is_expired:
            raise AuthError('token expired')

        self._validated = True
        return self

    @property
    def tenant(self) -> Optional[str]:
        """the tenant id asserted by the token"""
        return self.token_data.get('tenant', None)

    @property
    def domain(self) -> Optional[str]:
        """the waylay domain asserted by the token"""
        return self.token_data.get('domain', None)

    @property
    def subject(self) -> Optional[str]:
        """the subject asserted by the token"""
        return self.token_data.get('sub', None)

    @property
    def licenses(self) -> List[str]:
        """the licenses asserted by the token"""
        return self.token_data.get('licenses', [])

    @property
    def groups(self) -> List[str]:
        """the groups asserted by the token"""
        return self.token_data.get('groups', [])

    @property
    def permissions(self) -> List[str]:
        """the permissions asserted by the token"""
        return self.token_data.get('permissions', [])

    @property
    def expires_at(self) -> Optional[datetime]:
        """the token expiry timestamp"""
        exp = self.token_data.get('exp', None)
        return None if exp is None else datetime.fromtimestamp(exp)

    @property
    def is_expired(self) -> bool:
        """true if a (previously valid) the token has expired"""
        if not isinstance(self.token_data, dict):
            return True
        exp = self.expires_at
        return exp is None or exp < datetime.now()

    @property
    def is_valid(self) -> bool:
        """true if the token has been validated and is not expired"""
        return self._validated and not self.is_expired

    def to_dict(self):
        """returns the main attributes of this token"""
        return dict(
            tenant=self.tenant,
            domain=self.domain,
            subject=self.subject,
            expires_at=str(self.expires_at),
            is_valid=self.is_valid
        )

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}({json.dumps(self.to_dict())})>'

    def __str__(self) -> str:
        return self.token_string

    def __bool__(self) -> bool:
        return self.is_valid


class WaylayTokenAuth(_http.Auth):
    """Authentication flow with a waylay token, will automatically refresh an expired token"""
    current_token: Optional[WaylayToken]
    credentials: WaylayCredentials

    def __init__(
        self,
        credentials: WaylayCredentials,
        initial_token: Optional[TokenString] = None,
        interactive: Callable[[], WaylayCredentials] = None
    ):
        self.credentials = credentials
        self.current_token = None

        if isinstance(credentials, TokenCredentials):
            initial_token = initial_token or credentials.token

        if initial_token:
            self.current_token = WaylayToken(initial_token).validate(credentials.accounts_url)

        self.interactive = interactive

    def auth_flow(self, request: _http.Request) -> Generator[_http.Request,  _http.Response, None]:
        """implements the authentication callback for the http client"""

        token = self.assure_valid_token()
        request.headers["Authorization"] = f"Bearer {token}"
        yield request

    def assure_valid_token(self) -> WaylayToken:
        """validate the current token and request a new one if invalid"""

        if self.current_token:
            # token exists and is valid
            return self.current_token

        self.current_token = self._request_token().validate(self.credentials.accounts_url)
        return self.current_token

    def _request_token(self) -> WaylayToken:
        """request a token"""

        if isinstance(self.credentials, NoCredentials):
            if self.interactive is not None:
                self.credentials = self.interactive()

        if isinstance(self.credentials, TokenCredentials):
            raise AuthError(
                f"cannot refresh expired token with credentials "
                f"of type '{self.credentials.credentials_type}'"
            )

        if isinstance(self.credentials, ApplicationCredentials):
            raise AuthError(
                f"credentials of type {self.credentials.credentials_type} are not supported yet"
            )

        if isinstance(self.credentials, ClientCredentials):
            token_url = f"{self.credentials.accounts_url}/tokens?grant_type=client_credentials"
            token_req = {
                'clientId': self.credentials.api_key,
                'clientSecret': self.credentials.api_secret,
            }
            try:
                token_resp = _http.post(url=token_url, json=token_req)
                token_resp.raise_for_status()
                token_resp_json = token_resp.json()
            except _http.HTTPError as exc:
                raise AuthError(f'could not obtain waylay token: {exc}') from exc
            return WaylayToken(token_resp_json['token'])

        raise AuthError(
            f"credentials of type {self.credentials.credentials_type} are not supported"
        )


_AUTH_MESSAGE_FOR_EXCEPTON_CLASS = [
    (jwt_exc.InvalidSignatureError, 'invalid token'),
    (jwt_exc.ExpiredSignatureError, 'token expired'),
    (jwt_exc.InvalidAudienceError, 'token assertion failed'),
    (jwt_exc.InvalidIssuerError, 'token assertion failed'),
    (jwt_exc.InvalidIssuedAtError, 'token assertion failed'),
    (jwt_exc.ImmatureSignatureError, 'invalid token'),
    (jwt_exc.InvalidKeyError, 'invalid token'),
    (jwt_exc.InvalidAlgorithmError, 'invalid token'),
    (jwt_exc.MissingRequiredClaimError, 'token assertion failed'),
    (jwt_exc.InvalidTokenError, 'invalid token'),
    (jwt_exc.PyJWTError, 'could not decode token'),
    (TypeError, 'could not decode token'),
    (ValueError, 'could not decode token')
]


def _auth_message_for_exception(exception):
    for (exc_class, msg) in _AUTH_MESSAGE_FOR_EXCEPTON_CLASS:
        if isinstance(exception, exc_class):
            return msg
    return 'could not decode token'


def parse_credentials(json_obj: Dict[str, Any]) -> WaylayCredentials:
    """convert a parsed json representation to a WaylayCredentials object"""

    cred_type = json_obj.get('type', None)
    if cred_type is None:
        raise ValueError('invalid json for credentials: missing type')

    for clz in [NoCredentials, ClientCredentials, ApplicationCredentials, TokenCredentials]:
        if clz.credentials_type == cred_type:  # type: ignore
            return clz(**{k: v for k, v in json_obj.items() if k != 'type'})

    raise ValueError(f'cannot parse json for credential type {cred_type}')
