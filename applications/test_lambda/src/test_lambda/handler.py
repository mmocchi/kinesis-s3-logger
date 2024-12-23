import os
import json
from my_logger.logger import LogData
from my_logger.logger import MyLogger
from my_logger.exceptions import LogWriteError

DELIVERY_STREAM_NAME = os.environ["DELIVERY_STREAM_NAME"]
logger = MyLogger(
    destination_name=DELIVERY_STREAM_NAME,
)


def lambda_handler(event, context):
    try:
        log_data = LogData.create(
            user_id="User00001", action="XXXXXXXXX API", details={}
        )
        logger.write_log(log_data)

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
