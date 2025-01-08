import uuid
from datetime import datetime
from typing import Any

import pytest
from my_logger.models import (
    AccessInfo,
    LogData,
    Parameter,
    RequestInfo,
    ResultInfo,
    UserInfo,
)


def _create_log_data() -> LogData:
    return LogData(
        id=uuid.uuid4(),
        timestamp=datetime.now(),
        user_info=UserInfo(user_id="User00001", user_name="User00001"),
        access_info=[
            AccessInfo(
                text="テストテキスト",
            )
        ],
        request_info=RequestInfo(
            request_id="Request00001",
            endpoint="get_user_info",
            method="GET",
            parameters=[
                Parameter(key="user_name", value="太郎"),
                Parameter(key="user_age", value="20"),
            ],
        ),
        result_info=ResultInfo(status="SUCCESS", error_message=None),
    )


@pytest.fixture
def sample_log_data() -> LogData:
    return _create_log_data()


@pytest.fixture
def sample_log_dict() -> dict[str, Any]:
    return _create_log_data().to_dict()


@pytest.fixture
def mock_kinesis_response() -> dict[str, Any]:
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
