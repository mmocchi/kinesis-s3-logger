import pytest
from typing import Dict, Any


@pytest.fixture
def sample_log_data() -> Dict[str, Any]:
    return {
        "user_id": "test_user",
        "action": "test_action",
        "details": {"key": "value"},
    }


@pytest.fixture
def mock_kinesis_response() -> Dict[str, str]:
    return {"RecordId": "test-record-id-12345"}


@pytest.fixture
def mock_boto3_client(mocker):
    mock_client = mocker.patch("boto3.client")
    mock_firehose = mocker.Mock()
    mock_client.return_value = mock_firehose
    return mock_firehose


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("test_lambda.handler.logger")
