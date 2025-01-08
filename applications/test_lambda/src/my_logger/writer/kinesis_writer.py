import boto3
import json
from typing import Any
from botocore.exceptions import BotoCoreError
from my_logger.exceptions import KinesisWriteError
from my_logger.interfaces import LogWriter


class KinesisWriter(LogWriter):
    """Kinesis Firehoseへのログ出力実装"""

    def __init__(self, delivery_stream_name: str) -> None:
        """
        Kinesis Firehoseクライアントを初期化する

        Args:
            delivery_stream_name: Firehoseの配信ストリーム名
        """
        self.firehose = boto3.client("firehose")
        self.delivery_stream_name = delivery_stream_name

    def write_log(self, log_data: dict[str, Any]) -> None:
        """
        JSONデータをKinesis Firehoseに書き込む

        Args:
            log_data: 書き込むJSONデータ

        Raises:
            KinesisWriteError: Firehoseへの書き込みに失敗した場合
        """
        try:
            json_data = json.dumps(log_data) + "\n"

            response = self.firehose.put_record(
                DeliveryStreamName=self.delivery_stream_name, Record={"Data": json_data}
            )

            return response["RecordId"]

        except (BotoCoreError, KeyError) as e:
            raise KinesisWriteError(str(e), e)
