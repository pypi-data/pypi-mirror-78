"""REST definitions for the 'series' entity of the 'data' service"""

from .._base import WaylayResource
from .._decorators import (
    exception_decorator,
    return_body_decorator
)

DEFAULT_DECORATORS = [exception_decorator, return_body_decorator]


class SeriesResource(WaylayResource):
    """REST Resource for the 'series' entity of the 'data' service"""
    actions = {
        'query': {
            'method': 'GET', 'url': '/resources/{}/series/{}',
            'decorators': DEFAULT_DECORATORS},
        'last': {
            'method': 'GET', 'url': '/resources/{}/series/{}/last',
            'decorators': DEFAULT_DECORATORS},
        'aggregate': {
            'method': 'POST', 'url': '/series/query',
            'decorators': DEFAULT_DECORATORS},
        'remove': {
            'method': 'DELETE', 'url': '/resources/{}',
            'decorators': DEFAULT_DECORATORS},
    }
