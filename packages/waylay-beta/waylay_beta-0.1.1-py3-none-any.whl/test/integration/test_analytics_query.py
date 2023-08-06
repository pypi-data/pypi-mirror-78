"""integration tests for waylay.service.analytics module"""
import csv
import pytest
from waylay import (
    WaylayClient
)

def test_analytics_query_json(waylay_test_client: WaylayClient):
    "execute query with json response"
    data_resp = waylay_test_client.analytics.query.data('151CF-temperature', raw=True).body
    assert data_resp is not None
    assert 'data' in data_resp
    assert len(data_resp['data']) == 1
    assert 'columns' in data_resp['data'][0]

def test_analytics_query_csv(waylay_test_client: WaylayClient):
    "execute query with json response"
    query = waylay_test_client.analytics.query.get('151CF-temperature', raw=True).body['query']
    data_resp = waylay_test_client.analytics.query.data('151CF-temperature', raw=True, params={'render.mode':'RENDER_MODE_CSV'}).body
    assert isinstance(data_resp, str)
    reader = csv.reader(data_resp.splitlines(), delimiter=',' )
    header = next(reader)
    assert isinstance(header, list)
    potential_column_names = ['timestamp'] + [ 
        s.get('name', s.get('resource',query.get('resource')) + '/' + s.get('metric',query.get('metric') )) for s in query['data']
    ]
    for col in header:
        assert col in potential_column_names
    