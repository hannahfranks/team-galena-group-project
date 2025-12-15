#Eventbridge trigger for ingestion

resource "aws_cloudwatch_event_rule" "schedule_ingestion_lambda" {
    name = "database-ingestion-schedule"
    schedule_expression = "rate(1 minute)"
}

resource "aws_cloudwatch_event_target" "ingestion_lambda" {
    rule = aws_cloudwatch_event_rule.schedule_ingestion_lambda.name
    arn = aws_lambda_function.ingestion_lambda.arn
}

resource "aws_lambda_permission" "eventbridge" {
    statement_id = "AllowEventBridgeInvoke"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.ingestion_lambda.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.schedule_ingestion_lambda.arn
}