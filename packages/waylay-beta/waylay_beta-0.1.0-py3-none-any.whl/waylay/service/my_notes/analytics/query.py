"""definitions for the 'query' entity of the 'analytics' Service"""

from .._base import WaylayResource
from .._decorators import return_body_decorator
from ._decorators import (
    analytics_exception_decorator,
    analytics_return_dataframe_decorator,
    MultiFrameHandling
)

CONFIG_ENTITY_DECORATORS = [
    analytics_exception_decorator, return_body_decorator
]
DATA_RESPONSE_DECORATORS = [
    analytics_exception_decorator,
    analytics_return_dataframe_decorator(
        'data',
        default_frames_handling=MultiFrameHandling.JOIN
    )
]


class QueryResource(WaylayResource):
    """REST Resource for the 'query' entity of the 'analytics' Service"""
    actions = {
        'list': {
            'method': 'GET', 'url': '/config/query', 'decorators': CONFIG_ENTITY_DECORATORS},
        'create': {
            'method': 'POST', 'url': '/config/query', 'decorators': CONFIG_ENTITY_DECORATORS},
        'get': {
            'method': 'GET', 'url': '/config/query/{}', 'decorators': CONFIG_ENTITY_DECORATORS},
        'remove': {
            'method': 'DELETE', 'url': '/config/query/{}', 'decorators': CONFIG_ENTITY_DECORATORS},
        'replace': {
            'method': 'PUT', 'url': '/config/query/{}', 'decorators': CONFIG_ENTITY_DECORATORS},
        'data': {
            'method': 'GET', 'url': '/data/query/{}', 'decorators': DATA_RESPONSE_DECORATORS},
        'execute': {
            'method': 'POST', 'url': '/data/query', 'decorators': DATA_RESPONSE_DECORATORS},
    }
