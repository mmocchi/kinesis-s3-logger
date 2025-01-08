import json
import os
import uuid
from datetime import datetime

from my_logger.exceptions import LogWriteError
from my_logger.logger_factory import LoggerFactory
from my_logger.models import (
    AccessInfo,
    LogData,
    Parameter,
    RequestInfo,
    ResultInfo,
    UserInfo,
)

DELIVERY_STREAM_NAME = os.environ["DELIVERY_STREAM_NAME"]
logger = LoggerFactory.create_both_logger(DELIVERY_STREAM_NAME)


def lambda_handler(event, context):
    try:
        log_data = create_log_data()
        logger.info(log_data)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Log written successfully",
                }
            ),
        }

    except LogWriteError as e:
        raise e
    except Exception as e:
        raise e


def create_log_data():
    return LogData(
        id=uuid.uuid4(),
        timestamp=datetime.now(),
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
        access_info=[
            AccessInfo(
                text="テストテキスト",
            )
        ],
        result_info=ResultInfo(status="SUCCESS", error_message=None),
    )
