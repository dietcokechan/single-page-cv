provider "aws" {
  region = "eu-north-1"
}

resource "aws_s3_bucket" "resume_bucket" {
  bucket = "singlepagecvbucket"
  website {
    index_document = "index.html"
  }
}

resource "aws_dynamodb_table" "visitor_counter" {
  name           = "VisitorCounter"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "visitorId"

  attribute {
    name = "visitorId"
    type = "S"
  }
}

resource "aws_lambda_function" "visitor_lambda" {
  function_name = "VisitorCounterFunction"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "index.handler"
  runtime       = "python3.12"
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.visitor_counter.name
    }
  }
}
