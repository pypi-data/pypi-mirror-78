"""REST definitions for version status of Waylay Analytics service"""

from .._base import WaylayResource
from .._decorators import (
    exception_decorator,
    return_body_decorator
)

DEFAULT_DECORATORS = [exception_decorator, return_body_decorator]


class VersionResource(WaylayResource):
    """static version/health endpoint"""
    actions = {
        'get': {'method': 'GET', 'url': '/', 'decorators': DEFAULT_DECORATORS}
    }
