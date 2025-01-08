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
            ├── glue.tf
            ├── athena.tf
            └── variables.tf
```

## requirements
- AWS Lambda
- AWS Kinesis firehose
- AWS S3
- AWS Athena
- python 3.9
- uv
- terraform
- mise
- task


## ログサンプル
```json
{
  "id": "eaab0e21-d581-44bf-bc40-2f336757162a",
  "timestamp": "2025-01-08T15:43:44.562643",
  "userInfo": {
    "userId": "User00001",
    "userName": "User00001"
  },
  "requestInfo": {
    "requestId": "Request00001",
    "endpoint": "get_user_info",
    "method": "GET",
    "parameters": [
      {
        "key": "user_name",
        "value": "太郎"
      },
      {
        "key": "user_age",
        "value": "20"
      }
    ]
  },
  "accessInfo": [
    {
      "text": "テストテキスト"
    }
  ],
  "resultInfo": {
    "status": "SUCCESS",
    "errorMessage": null
  }
}
```

## Athenaのクエリサンプル

### ユーザーで抽出

```sql
SELECT 
  id,
  timestamp,
  userinfo.username,
  requestinfo.endpoint,
  requestinfo.method,
  resultinfo.status
FROM application_logs
WHERE userinfo.username = 'User00001'
  AND year = '2024'
  AND month = '01'
ORDER BY timestamp DESC
LIMIT 100;
```

### parametersの値で抽出

```sql
SELECT 
  timestamp,
  userinfo.username,
  requestinfo.endpoint,
  requestinfo.method,
  param.key as parameter_key,
  param.value as parameter_value,
  resultinfo.status
FROM "application_logs"
CROSS JOIN UNNEST(requestinfo.parameters) AS t(param)
WHERE param.key = 'user_name'
  AND param.value = '太郎'
  AND year = '2025'
  AND month = '01'
ORDER BY timestamp DESC;
```

### 正規表現を使用した検索（より柔軟なパターンマッチング）

```sql
SELECT 
  timestamp,
  userinfo.username,
  requestinfo.endpoint,
  param.value as user_name
FROM "${var.environment}_${var.project}_logs"."application_logs"
CROSS JOIN UNNEST(requestinfo.parameters) AS t(param)
WHERE param.key = 'user_name'
  AND REGEXP_LIKE(param.value, '佐藤|鈴木')  -- 複数のパターンにマッチ
  AND year = '2025'
  AND month = '01'
ORDER BY timestamp DESC;
```