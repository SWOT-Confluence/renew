# AWS Lambda function
resource "aws_lambda_function" "aws_lambda_renew" {
  filename         = "renew.zip"
  function_name    = "${var.prefix}-renew"
  role             = aws_iam_role.aws_lambda_renew_execution_role.arn
  handler          = "renew.handler"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256("renew.zip")
  timeout          = 300
}

# AWS Lambda execution role & policy
resource "aws_iam_role" "aws_lambda_renew_execution_role" {
  name = "${var.prefix}-lambda-renew-execution-role"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "lambda.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })
}

# Parameter Store policy
resource "aws_iam_role_policy_attachment" "aws_lambda_get_put_parameter_policy_attach" {
  role       = aws_iam_role.aws_lambda_renew_execution_role.name
  policy_arn = data.aws_iam_policy.get_put_parameter.arn
}

# Execution policy
resource "aws_iam_role_policy_attachment" "aws_lambda_renew_execution_role_policy_attach" {
  role       = aws_iam_role.aws_lambda_renew_execution_role.name
  policy_arn = aws_iam_policy.aws_lambda_renew_execution_policy.arn
}

resource "aws_iam_policy" "aws_lambda_renew_execution_policy" {
  name        = "${var.prefix}-lambda-renew-execution-policy"
  description = "Upload files to bucket and send messages to queue."
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "AllowCreatePutLogs",
        "Effect" : "Allow",
        "Action" : [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# EventBridge schedule
resource "aws_scheduler_schedule" "aws_schedule_renew_aqua" {
  name       = "${var.prefix}-renew"
  group_name = "default"
  flexible_time_window {
    mode = "OFF"
  }
  schedule_expression = "rate(50 minutes)"
  target {
    arn      = aws_lambda_function.aws_lambda_renew.arn
    role_arn = aws_iam_role.aws_eventbridge_renew_execution_role.arn
  }
  state = "DISABLED"
}

# EventBridge execution role and policy
resource "aws_iam_role" "aws_eventbridge_renew_execution_role" {
  name = "${var.prefix}-eventbridge-renew-execution-role"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "scheduler.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "aws_eventbridge_renew_execution_role_policy_attach" {
  role       = aws_iam_role.aws_eventbridge_renew_execution_role.name
  policy_arn = aws_iam_policy.aws_eventbridge_renew_execution_policy.arn
}

resource "aws_iam_policy" "aws_eventbridge_renew_execution_policy" {
  name        = "${var.prefix}-eventbridge-renew-execution-policy"
  description = "Allow EventBridge to invoke a Lambda function."
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "AllowInvokeLambda",
        "Effect" : "Allow",
        "Action" : [
          "lambda:InvokeFunction"
        ],
        "Resource" : "${aws_lambda_function.aws_lambda_renew.arn}"
      }
    ]
  })
}