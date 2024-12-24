from my_logger.formatter.json_formatter import JsonFormatter
from my_logger.models import LogData
import re


def test_json_formatter():
    input_log_data = {
        "user_id": "123",
        "action": "test",
        "details": {"key": "value"},
    }

    formatter = JsonFormatter()
    log_data = LogData.create(**input_log_data)
    formatted_log = formatter.format(log_data)

    expected_log_data = {
        "timestamp": "2024-01-01T00:00:00Z",
        "user_id": "123",
        "action": "test",
        "details": {"key": "value"},
    }
    assert formatted_log["action"] == expected_log_data["action"]
    assert formatted_log["details"] == expected_log_data["details"]
    assert formatted_log["user_id"] == expected_log_data["user_id"]

    # タイムスタンプはISO形式の日付フォーマットの文字列で返されることを正規表現で確認
    assert re.match(
        r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}$", formatted_log["timestamp"]
    )
