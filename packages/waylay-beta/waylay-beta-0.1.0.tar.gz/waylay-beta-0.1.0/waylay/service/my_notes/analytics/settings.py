"""REST definitions for the settings of the Waylay Analytics service"""

from .._base import WaylayResource
from .._decorators import (
    exception_decorator,
    return_body_decorator
)

DEFAULT_DECORATORS = [exception_decorator, return_body_decorator]


class SettingsResource(WaylayResource):
    """server settings"""
    actions = {
        'get': {
            'method': 'GET', 'url': '/static/settings',
            'decorators': DEFAULT_DECORATORS
        }
    }
