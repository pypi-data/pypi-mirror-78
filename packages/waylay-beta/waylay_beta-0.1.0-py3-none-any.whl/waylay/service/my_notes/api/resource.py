"""REST definitions for the resource entity of the api service"""

from .._base import WaylayResource
from .._decorators import (
    exception_decorator,
    return_body_decorator
)

DEFAULT_DECORATORS = [exception_decorator, return_body_decorator]


class ResourceResource(WaylayResource):
    """REST Resource for the resource entity of the api service"""
    actions = {
        'get': {
            'method': 'GET',
            'url': '/api/resources/{id}',
            'decorators': DEFAULT_DECORATORS},
        'create': {
            'method': 'POST',
            'url': '/api/resources',
            'decorators': DEFAULT_DECORATORS},
        'update': {
            'method': 'PATCH',
            'url': '/api/resources/{id}',
            'decorators': DEFAULT_DECORATORS},
        'replace': {
            'method': 'PUT',
            'url': '/api/resources/{id}',
            'decorators': DEFAULT_DECORATORS},
        'remove': {
            'method': 'DELETE',
            'url': '/api/resources/{id}',
            'decorators': DEFAULT_DECORATORS},
        'search': {
            'method': 'GET',
            'url': '/api/resources?{params}',
            'decorators': DEFAULT_DECORATORS},
    }
