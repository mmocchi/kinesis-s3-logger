import os
os.environ["DELIVERY_STREAM_NAME"] = "test-kinesis-stream-name"


import pytest
from test_lambda.handler import lambda_handler
from my_logger.exceptions import LogWriteError


def test_lambda_handler_success(mock_logger):
    """
    lambda_handlerの成功パターンのテスト
    
    期待される動作:
    - ステータスコード200が返却されること
    - レスポンスボディにメッセージが含まれること
    - loggerのwrite_logが1回呼び出されること
    """
    # Arrange
    expected_status_code = 200
    
    # Act
    response = lambda_handler(None, None)
    
    # Assert
    assert response["statusCode"] == expected_status_code
    assert "message" in response["body"]
    mock_logger.write_log.assert_called_once()

def test_lambda_handler_log_write_error(mock_logger):
    """
    lambda_handlerのログ書き込みエラーパターンのテスト
    
    期待される動作:
    - ログ書き込みエラー時にLogWriteErrorが発生すること
    """
    # Arrange
    mock_logger.write_log.side_effect = LogWriteError("Test error", Exception())
    
    # Act & Assert
    with pytest.raises(LogWriteError):
        lambda_handler(None, None) 