"""definitions for the 'query' entity of the 'analytics' Service"""

from .._base import WaylayResource
from .._decorators import (
    return_path_decorator
)
from ._decorators import (
    analytics_exception_decorator,
    analytics_return_dataframe_decorator,
    MultiFrameHandling
)


def parse_query_entity(json_dict: dict):
    """default response constructor for query config entities"""
    return json_dict


CONFIG_ENTITY_DECORATORS = [
    analytics_exception_decorator,
    return_path_decorator(['query'], parse_query_entity)
]

CONFIG_LIST_DECORATORS = [
    analytics_exception_decorator,
    return_path_decorator(['queries', 'name'])
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
            'method': 'GET', 'url': '/config/query', 'decorators': CONFIG_LIST_DECORATORS},
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
