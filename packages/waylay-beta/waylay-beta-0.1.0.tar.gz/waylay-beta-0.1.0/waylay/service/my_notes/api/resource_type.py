"""REST definitions for the 'resource_type' entity of the 'api' service"""

from .._base import WaylayResource
from .._decorators import (
    exception_decorator,
    return_body_decorator
)

DEFAULT_DECORATORS = [exception_decorator, return_body_decorator]


class ResourceTypeResource(WaylayResource):
    """REST Resource for the 'resource_type' entity of the 'api' service"""
    actions = {
        'create': {
            'method': 'POST', 'url': '/api/resourcetypes', 'decorators': DEFAULT_DECORATORS},
        'remove': {
            'method': 'DELETE', 'url': '/api/resourcetypes/{id}', 'decorators': DEFAULT_DECORATORS},
        'replace': {
            'method': 'PUT', 'url': '/api/resourcetypes/{id}', 'decorators': DEFAULT_DECORATORS},
        'update': {
            'method': 'PATCH', 'url': '/api/resourcetypes/{id}', 'decorators': DEFAULT_DECORATORS},
        'get': {
            'method': 'GET', 'url': '/api/resourcetypes/{id}', 'decorators': DEFAULT_DECORATORS},
        'list': {
            'method': 'GET', 'url': '/api/resourcetypes', 'decorators': DEFAULT_DECORATORS},
    }
