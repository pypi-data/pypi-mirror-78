"""REST definitions for the use case operations of the Waylay Analytics service"""

from .._base import WaylayResource
from .._decorators import return_body_decorator
from ._decorators import (
    analytics_exception_decorator,
    analytics_return_dataframe_decorator,
    MultiFrameHandling
)

JSON_DECORATORS = [
    analytics_exception_decorator, return_body_decorator
]
DATAFRAME_DECORATORS = [
    analytics_exception_decorator,
    analytics_return_dataframe_decorator(
        data_key='data',
        default_frames_handling=MultiFrameHandling.JOIN
    )
]
DEFAULT_ANALYTICS_USECASE_TIMEOUT = 180  # seconds


class UseCaseResource(WaylayResource):
    """Base class for the usecase resources"""

    def __init__(self, *args, **kwargs):
        kwargs.pop('timeout', None)
        super().__init__(*args, timeout=DEFAULT_ANALYTICS_USECASE_TIMEOUT, **kwargs)


class PredictResource(UseCaseResource):
    """REST Resource for the 'predict' entity of the 'analytics' service"""
    actions = {
        'execute': {
            'method': 'POST', 'url': '/predict', 'decorators': DATAFRAME_DECORATORS
        },
    }


class AnomalyResource(UseCaseResource):
    """REST Resource for the 'anomaly' entity of the 'analytics' service"""
    actions = {
        'execute': {
            'method': 'POST', 'url': '/anomaly', 'decorators': DATAFRAME_DECORATORS
        },
    }


class ValidateResource(UseCaseResource):
    """REST Resource for the 'validate' entity of the 'analytics' service"""
    actions = {
        'execute': {
            'method': 'POST', 'url': '/validate', 'decorators': JSON_DECORATORS
        },
    }


class FitResource(UseCaseResource):
    """REST Resource for the 'fit' entity of the 'analytics' service"""
    actions = {
        'execute': {
            'method': 'POST', 'url': '/fit', 'decorators': DATAFRAME_DECORATORS
        },
    }


class EstimateResource(UseCaseResource):
    """REST Resource for the 'estimate' entity of the 'analytics' service"""
    actions = {
        'execute': {
            'method': 'POST', 'url': '/estimate', 'decorators': DATAFRAME_DECORATORS
        },
    }


class ModelSearchResource(UseCaseResource):
    """REST Resource for the 'model_search' entity of the 'analytics' service"""
    actions = {
        'execute': {
            'method': 'POST', 'url': '/model_search', 'decorators': JSON_DECORATORS
        },
    }


class DataResource(UseCaseResource):
    """REST Resource for the 'data' entity of the 'analytics' service"""
    actions = {
        'execute': {
            'method': 'POST', 'url': '/data', 'decorators': DATAFRAME_DECORATORS
        },
    }


class DataSummaryResource(UseCaseResource):
    """REST Resource for the 'data_summary' entity of the 'analytics' service"""
    actions = {
        'execute': {
            'method': 'POST', 'url': '/data_summary', 'decorators': JSON_DECORATORS
        },
    }
