from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any, Optional
from my_logger.protocols import LogWriter
from my_logger.kinesis_client import KinesisWriter
from typing import overload

@dataclass
class LogData:
    """ログデータの構造を表現するデータクラス"""
    timestamp: str
    user_id: str
    action: str
    details: Dict[str, Any]

    @classmethod
    def create(
        cls,
        user_id: str,
        action: str,
        details: Optional[Dict[str, Any]] = None
    ) -> 'LogData':
        """新しいログデータインスタンスを作成する"""
        return cls(
            timestamp=datetime.now().isoformat(),
            user_id=user_id,
            action=action,
            details=details or {}
        )

    def to_dict(self) -> Dict[str, Any]:
        """ログデータを辞書に変換する"""
        return asdict(self)

class MyLogger:
    def __init__(self, destination_name: str) -> None:
        """
        ロガーを初期化する
        
        Args:
            destination_name: 格納先の名称
        """
        self.log_writer: LogWriter = KinesisWriter(destination_name)

    def write_log(
        self,
        log_data: LogData
    ) -> None:
        """
        ログを書き込む
        
        Args:
            user_id: ユーザーID
            action: 実行されたアクション
            details: 追加のログ情報
                        
        Raises:
            boto3.exceptions.Boto3Error: ログの書き込みに失敗した場合
        """
        self.log_writer.write_log(log_data.to_dict())
