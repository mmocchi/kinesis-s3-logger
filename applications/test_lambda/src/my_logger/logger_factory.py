from my_logger.formatter.json_formatter import JsonFormatter
from my_logger.interfaces import Logger
from my_logger.logger import MultiLogger, MyLogger
from my_logger.writer.console_writer import ConsoleWriter
from my_logger.writer.kinesis_writer import KinesisWriter


class LoggerFactory:
    """Loggerのファクトリークラス"""

    @staticmethod
    def create_kinesis_logger(destination_name: str) -> Logger:
        """
        Kinesis Firehoseへのログ出力を行うLoggerを作成する

        Args:
            destination_name (str): Kinesis Firehoseの配信ストリーム名

        Returns:
            Logger: Kinesis Firehoseへのログ出力を行うLogger
        """
        writer = KinesisWriter(destination_name)
        formatter = JsonFormatter()
        return MyLogger(writer, formatter)

    @staticmethod
    def create_console_logger() -> Logger:
        """
        標準出力へのログ出力を行うLoggerを作成する

        Returns:
            Logger: 標準出力へのログ出力を行うLogger
        """
        writer = ConsoleWriter()
        formatter = JsonFormatter()
        return MyLogger(writer, formatter)

    @staticmethod
    def create_both_logger(destination_name: str) -> Logger:
        """
        Kinesis Firehoseと標準出力へのログ出力を行うLoggerを作成する

        Args:
            destination_name (str): Kinesis Firehoseの配信ストリーム名

        Returns:
            Logger: Kinesis Firehoseと標準出力へのログ出力を行うLogger
        """
        return MultiLogger(
            [
                LoggerFactory.create_kinesis_logger(destination_name),
                LoggerFactory.create_console_logger(),
            ]
        )
