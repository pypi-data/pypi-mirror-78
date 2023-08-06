
"""REST client for the Waylay Time Series Analytics Service"""

from .._base import WaylayService

from .model import ModelResource
from .status import StatusResource


class ByomlService(WaylayService):
    """REST client for the Waylay BYOML Service"""
    config_key = 'byoml'
    default_root_url = 'https://byoml.waylay.io'
    resource_definitions = {
        'model': ModelResource,
        'status': StatusResource
    }

    model: ModelResource
    status: StatusResource

    def __init__(self):
        super().__init__(
            json_encode_body=True
        )
