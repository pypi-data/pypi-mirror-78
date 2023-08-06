"""REST definitions for the 'message' entity of the 'data' service"""

from .._base import WaylayResource
from .._decorators import (
    exception_decorator,
    return_body_decorator
)

DEFAULT_DECORATORS = [exception_decorator, return_body_decorator]


class MessageResource(WaylayResource):
    """REST Resource for the 'message' entity of the 'data' service"""
    actions = {
        'send': {
            'method': 'POST', 'url': '/resources/{}', 'decorators': DEFAULT_DECORATORS},
        'send_bulk': {
            'method': 'POST', 'url': '/messages', 'decorators': DEFAULT_DECORATORS},
        'get': {
            'method': 'GET', 'url': '/resources/{}/series', 'decorators': DEFAULT_DECORATORS},
        'query': {
            'method': 'POST', 'url': '/messages/query', 'decorators': DEFAULT_DECORATORS},
        'current': {
            'method': 'GET', 'url': '/resources/{}/current', 'decorators': DEFAULT_DECORATORS},
        'last': {
            'method': 'GET', 'url': '/resources/{}/messages', 'decorators': DEFAULT_DECORATORS},
    }
