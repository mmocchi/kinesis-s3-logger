from my_logger.models import LogData
from my_logger.factory import LoggerFactory
from my_logger.formatter.json_formatter import JsonFormatter


def test_my_logger_write_log(mocker, sample_log_data):
    """
    MyLogger.write_logメソッドのテスト

    期待される動作:
    - LogDataオブジェクトが正しく辞書形式に変換されてlog_writerに渡されること
    - log_writerのwrite_logメソッドが1回だけ呼び出されること
    """
    # Arrange
    mock_writer = mocker.Mock()
    mock_writer.write_log.return_value = "test-record-id"
    logger = LoggerFactory.create_kinesis_logger("test-stream")
    logger.writer = mock_writer
    log_data = LogData.create(**sample_log_data)

    formatter = JsonFormatter()
    formatted_log_data = formatter.format(log_data)

    # Act
    logger.info(log_data)

    # Assert
    mock_writer.write_log.assert_called_once_with(formatted_log_data)
