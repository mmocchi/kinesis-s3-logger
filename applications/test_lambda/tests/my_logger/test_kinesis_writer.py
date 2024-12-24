import pytest
from botocore.exceptions import BotoCoreError
from my_logger.writer.kinesis_writer import KinesisWriter
from my_logger.exceptions import KinesisWriteError


def test_kinesis_writer_write_log_success(
    mock_boto3_client, sample_log_data, mock_kinesis_response
):
    """
    KinesisWriter.write_logメソッドの成功パターンのテスト

    期待される動作:
    - boto3が適切に呼び出されていること
    """
    # Arrange
    mock_boto3_client.put_record.return_value = mock_kinesis_response
    writer = KinesisWriter("test-stream")
    expected_record_id = mock_kinesis_response["RecordId"]

    # Act
    record_id = writer.write_log(sample_log_data)

    # Assert
    assert record_id == expected_record_id
    mock_boto3_client.put_record.assert_called_once()


def test_kinesis_writer_write_log_error(mock_boto3_client):
    """
    KinesisWriter.write_logメソッドのエラーパターンのテスト

    期待される動作:
    - Kinesis書き込みエラー時(boto3エラー)にKinesisWriteErrorが発生すること
    """
    # Arrange
    mock_boto3_client.put_record.side_effect = BotoCoreError()
    writer = KinesisWriter("test-stream")
    test_data = {"test": "data"}

    # Act & Assert
    with pytest.raises(KinesisWriteError):
        writer.write_log(test_data)
