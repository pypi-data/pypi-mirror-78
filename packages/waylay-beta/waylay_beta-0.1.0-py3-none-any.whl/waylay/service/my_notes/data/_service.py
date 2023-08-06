
"""REST client for the Waylay Data Service (broker)"""

from .._base import WaylayService

from .message import MessageResource
from .series import SeriesResource


class DataService(WaylayService):
    """REST client for the Waylay Data Service (broker)"""
    config_key = 'data'
    default_root_url = 'https://data.waylay.io'
    resource_definitions = {
        'message': MessageResource,
        'series': SeriesResource
    }

    message: MessageResource
    series: SeriesResource
