import io
import json
import logging
from action_engine.logging.logger import JsonFormatter, get_logger


def create_logger():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger('test_logger')
    logger.handlers = []
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger, stream


def test_formatter_includes_timestamp_and_request_id():
    logger, stream = create_logger()
    logger.info('msg', extra={'request_id': '123'})
    data = json.loads(stream.getvalue())
    assert data['message'] == 'msg'
    assert 'time' in data
    assert data['request_id'] == '123'


def test_formatter_without_request_id():
    logger, stream = create_logger()
    logger.info('hello')
    data = json.loads(stream.getvalue())
    assert data['message'] == 'hello'
    assert 'time' in data
    assert 'request_id' not in data


def test_sanitize_token_filter_replaces_sensitive_values():
    """Logger obtained via get_logger should mask token-like fields."""
    logger = get_logger('token_test_logger')
    stream = io.StringIO()

    handler = logger.handlers[0]
    handler.stream = stream
    handler.setFormatter(logging.Formatter('%(access_token)s %(refresh_token)s'))

    logger.info('ignore', extra={'access_token': 'secret', 'refresh_token': 'r'})

    assert stream.getvalue().strip() == '*** ***'

