import datetime as dt
from my_logger.models import LogData


def test_代表的なLogDataを作成できること():
    """
    LogData.createメソッドのテスト

    期待される動作:
    - 与えられたパラメータから正しくLogDataインスタンスが生成されること
    - タイムスタンプが文字列として自動生成されること
    """

    # Arrange and Act
    log_data = LogData.create(
        user_id="test_user", action="test_action", details={"key": "value"}
    )

    # Assert
    assert log_data.user_id == "test_user"
    assert log_data.action == "test_action"
    assert log_data.details == {"key": "value"}

    assert isinstance(log_data.timestamp, dt.datetime)
