"""REST definitions for the 'model' entity of the 'analytics' service"""

from .._base import WaylayResource
from .._decorators import return_body_decorator
from ._decorators import (
    analytics_exception_decorator,
    analytics_return_dataframe_decorator,
    MultiFrameHandling
)

MODEL_CONFIG_DECS = [
    analytics_exception_decorator, return_body_decorator
]
MODEL_DATAFRAME_DECS = [
    analytics_exception_decorator,
    analytics_return_dataframe_decorator(
        data_key='data',
        default_frames_handling=MultiFrameHandling.JOIN
    )
]
DEFAULT_ANALYTICS_MODEL_TIMEOUT = 60


class ModelResource(WaylayResource):
    """REST Resource for the 'model' entity of the 'analytics' service"""
    actions = {
        'create': {
            'method': 'POST', 'url': '/config/{}', 'decorators': MODEL_CONFIG_DECS},
        'list': {
            'method': 'GET', 'url': '/config/{}', 'decorators': MODEL_CONFIG_DECS},
        'get': {
            'method': 'GET', 'url': '/config/{}/{}', 'decorators': MODEL_CONFIG_DECS},
        'remove': {
            'method': 'DELETE', 'url': '/config/{}/{}', 'decorators': MODEL_CONFIG_DECS},
        'update': {
            'method': 'PATCH', 'url': '/config/{}/{}', 'decorators': MODEL_CONFIG_DECS},
        'replace': {
            'method': 'PUT', 'url': '/config/{}/{}', 'decorators': MODEL_CONFIG_DECS},
        'predict': {
            'method': 'GET', 'url': '/predict/{}/{}', 'decorators': MODEL_DATAFRAME_DECS},
        'anomaly': {
            'method': 'GET', 'url': '/anomaly/{}/{}', 'decorators': MODEL_DATAFRAME_DECS},
        'validate': {
            'method': 'GET', 'url': '/validate/{}/{}', 'decorators': MODEL_DATAFRAME_DECS},
        'fit': {
            'method': 'GET', 'url': '/fit/{}/{}', 'decorators': MODEL_DATAFRAME_DECS},
        'estimate': {
            'method': 'GET', 'url': '/estimate/{}/{}', 'decorators': MODEL_DATAFRAME_DECS},
        'model_search': {
            'method': 'GET', 'url': '/model_search/{}/{}', 'decorators': MODEL_CONFIG_DECS},
        'data': {
            'method': 'GET', 'url': '/data/{}/{}', 'decorators': MODEL_DATAFRAME_DECS},
    }

    def __init__(self, *args, **kwargs):
        kwargs.pop('timeout', None)
        super().__init__(*args, timeout=DEFAULT_ANALYTICS_MODEL_TIMEOUT, **kwargs)
