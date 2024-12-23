# kinesis-s3-logger

LambdaからKinesis経由でS3にログを書き込むサンプル

## プロジェクト構造

```
.
├── README.md
├── applications
│   └── test_lambda             # Kinesisにログを書き込むサンプルのLambdaアプリケーション
│       ├── Taskfile.yml        # タスクランナー
│       ├── pyproject.toml
│       ├── src
│       │   ├── my_logger       # ロガーモジュール
│       │   └── test_lambda     # ロガーを使うLambda関数
│       ├── tests               # テストコード
│       │   ├── conftest.py
│       │   ├── my_logger
│       │   └── test_lambda
│       └── uv.lock
└── terraform                   # Terraformの設定
    ├── Taskfile.yml            # タスクランナー
    ├── environments            # 環境ごとの設定
    │   └── dev
    │       └── main.tf
    └── modules                 # モジュール
        └── log_infrastructure  # Lambda、KinesisとS3のインフラストラクチャー
            ├── kinesis.tf
            ├── lambda.tf
            ├── s3.tf
            └── variables.tf
```

## requirements
- AWS Lambda
- AWS Kinesis firehose
- AWS S3
- python 3.9
- uv
- terraform
- mise
- task


