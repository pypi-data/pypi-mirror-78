"""REST definitions for the Settings entity of the Waylay Engine Service"""

from .._base import WaylayResource
from .._decorators import (
    exception_decorator,
    return_body_decorator
)

DEFAULT_DECORATORS = [exception_decorator, return_body_decorator]


class SettingsResource(WaylayResource):
    """REST Resource for the Query entity of the Analytics Service"""
    actions = {
        'get': {
            'method': 'GET', 'url': '/api/settings',
            'decorators': DEFAULT_DECORATORS
        },
    }
