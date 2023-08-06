"""REST definitions for the 'task' entity of the 'analytics' service"""

from .._base import WaylayResource
from .._decorators import return_body_decorator
from ._decorators import analytics_exception_decorator

TASK_DECORATORS = [analytics_exception_decorator, return_body_decorator]


class TaskResource(WaylayResource):
    """REST Resource for the 'task' entity of the 'analytics' service"""
    actions = {
        'status': {
            'method': 'GET', 'url': '/task/{task_id}/status',
            'decorators': TASK_DECORATORS},
        'cancel': {
            'method': 'POST', 'url': '/task/{task_id}/cancel',
            'decorators': TASK_DECORATORS},
        'result': {
            'method': 'GET', 'url': '/task/{task_id}/query',
            'decorators': TASK_DECORATORS},
    }
