import uuid
from datetime import datetime

from my_logger.formatter.json_formatter import JsonFormatter
from my_logger.models import (
    AccessInfo,
    LogData,
    Parameter,
    RequestInfo,
    ResultInfo,
    UserInfo,
)


def create_log_data():
    return LogData(
        id=uuid.uuid4(),
        timestamp=datetime.fromisoformat("2024-01-01T00:00:00.000000+09:00"),
        user_info=UserInfo(user_id="User00001", user_name="User00001"),
        request_info=RequestInfo(
            request_id="Request00001",
            endpoint="get_user_info",
            method="GET",
            parameters=[
                Parameter(key="user_name", value="太郎"),
                Parameter(key="user_age", value="20"),
            ],
        ),
        access_info=[AccessInfo(text="AccessInfo00001")],
        result_info=ResultInfo(status="SUCCESS", error_message=None),
    )


def test_json_formatter():
    formatter = JsonFormatter()
    log_data = create_log_data()
    formatted_log = formatter.format(log_data)

    assert formatted_log["id"] == str(log_data.id)
    assert formatted_log["timestamp"] == "2024-01-01T00:00:00.000000+09:00"
    assert formatted_log["userInfo"]["userId"] == "User00001"
    assert formatted_log["userInfo"]["userName"] == "User00001"
    assert formatted_log["requestInfo"]["requestId"] == "Request00001"
    assert formatted_log["requestInfo"]["endpoint"] == "get_user_info"
    assert formatted_log["requestInfo"]["method"] == "GET"
    assert formatted_log["requestInfo"]["parameters"][0]["key"] == "user_name"
    assert formatted_log["requestInfo"]["parameters"][0]["value"] == "太郎"
    assert formatted_log["requestInfo"]["parameters"][1]["key"] == "user_age"
    assert formatted_log["requestInfo"]["parameters"][1]["value"] == "20"
    assert formatted_log["accessInfo"][0]["text"] == "AccessInfo00001"
    assert formatted_log["resultInfo"]["status"] == "SUCCESS"
    assert formatted_log["resultInfo"]["errorMessage"] is None
