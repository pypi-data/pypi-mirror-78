
"""REST client for the Waylay Time Series Analytics Service"""

from .._base import WaylayService

from .query import QueryResource
from .model import ModelResource
from .settings import SettingsResource
from .version import VersionResource
from .usecase import (
    FitResource,
    AnomalyResource,
    ValidateResource,
    PredictResource,
    EstimateResource,
    ModelSearchResource,
    DataResource,
    DataSummaryResource,
)
from .task import TaskResource


class AnalyticsService(WaylayService):
    """REST client for the Analytics Service"""
    config_key = 'analytics'
    default_root_url = 'https://ts-analytics.waylay.io'
    resource_definitions = {
        'query': QueryResource,
        'model': ModelResource,
        'version': VersionResource,
        'settings': SettingsResource,
        'fit': FitResource,
        'anomaly': AnomalyResource,
        'validate': ValidateResource,
        'predict': PredictResource,
        'estimate': EstimateResource,
        'model_search': ModelSearchResource,
        'data': DataResource,
        'data_summary': DataSummaryResource,
        'task': TaskResource
    }
    query: QueryResource
    model: ModelResource
    version: VersionResource
    settings: SettingsResource
    fit: FitResource
    anomaly: AnomalyResource
    validate: ValidateResource
    predict: PredictResource
    estimate: EstimateResource
    model_search: ModelSearchResource
    data: DataResource
    data_summary: DataSummaryResource
    task: TaskResource

    def __init__(self):
        super().__init__(
            json_encode_body=True,
            params={
                'api_version': '0.19',
                # 'render.mode': 'RENDER_MODE_SERIES', // conflicts with 'Accept: text/csv' !! bug?
                # 'json_validate_request': True
            }
        )
