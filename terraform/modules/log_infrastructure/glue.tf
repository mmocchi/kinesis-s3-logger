resource "aws_glue_catalog_database" "logs_db" {
  name        = "${var.environment}_${var.project}_logs"
  description = "Database for analyzing application logs"
}

resource "aws_glue_catalog_table" "logs_table" {
  name          = "application_logs"
  database_name = aws_glue_catalog_database.logs_db.name
  table_type    = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL                                  = "TRUE"
    "classification"                          = "json"
    "projection.enabled"                      = "true"
    "projection.partition_date.type"          = "date"
    "projection.partition_date.range"         = "NOW-1YEARS,NOW+2YEARS"
    "projection.partition_date.format"        = "yyyy-MM-dd"
    "projection.partition_date.interval"      = "1"
    "projection.partition_date.interval.unit" = "DAYS"
    "storage.location.template"               = "s3://${aws_s3_bucket.log_bucket.id}/logs/year=$${partition_date:yyyy}/month=$${partition_date:MM}/day=$${partition_date:dd}"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.log_bucket.id}/logs/"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"

    ser_de_info {
      name                  = "JsonSerDe"
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"
      parameters = {
        "serialization.format" = "1"
        "case.insensitive"     = "TRUE"
      }
    }

    # LogDataクラスの構造に基づくカラム定義
    columns {
      name = "id"
      type = "string"
    }
    columns {
      name = "timestamp"
      type = "timestamp"
    }
    # UserInfo
    columns {
      name = "userinfo"
      type = "struct<userid:string,username:string>"
    }
    # RequestInfo
    columns {
      name = "requestinfo"
      type = "struct<requestid:string,endpoint:string,method:string,parameters:array<struct<key:string,value:string>>>"
    }
    # AccessInfo
    columns {
      name = "accessinfo"
      type = "array<struct<text:string>>"
    }
    # ResultInfo
    columns {
      name = "resultinfo"
      type = "struct<status:string,errormessage:string>"
    }
  }

  # パーティション列の定義
  partition_keys {
    name = "year"
    type = "string"
  }
  partition_keys {
    name = "month"
    type = "string"
  }
  partition_keys {
    name = "day"
    type = "string"
  }
} 