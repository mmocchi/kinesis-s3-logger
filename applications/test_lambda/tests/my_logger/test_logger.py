import re
import datetime as dt
from my_logger.logger import LogData, MyLogger


def test_代表的なLogDataを作成できること():
    """
    LogData.createメソッドのテスト

    期待される動作:
    - 与えられたパラメータから正しくLogDataインスタンスが生成されること
    - タイムスタンプが文字列として自動生成されること
    """
    # Arrange
    pass

    # Act
    log_data = LogData.create(
        user_id="test_user", action="test_action", details={"key": "value"}
    )

    # Assert
    assert log_data.user_id == "test_user"
    assert log_data.action == "test_action"
    assert log_data.details == {"key": "value"}

    iso_format_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}$"
    assert isinstance(log_data.timestamp, str)
    assert re.match(iso_format_pattern, log_data.timestamp) is not None
    # 実際にパースできることを確認
    assert dt.datetime.fromisoformat(log_data.timestamp.replace("Z", "+00:00"))


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
    logger = MyLogger("test-stream")
    logger.log_writer = mock_writer
    log_data = LogData.create(**sample_log_data)

    # Act
    logger.write_log(log_data)

    # Assert
    mock_writer.write_log.assert_called_once_with(log_data.to_dict())
