from aws_cdk import (
    aws_apigateway as apigateway,
    Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_cloudwatch as cloudwatch,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_cloudwatch_actions as cloudwatch_actions,
    aws_lambda_event_sources as lambda_event_sources
)
from constructs import Construct

class Experimento1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

       # Crear la tabla DynamoDB
        table = dynamodb.Table(self, "Candidatos",
            partition_key=dynamodb.Attribute(
                name="email",
                type=dynamodb.AttributeType.STRING
            )
        )

        # Crear la capa de Lambda para las bibliotecas requeridas
        layer = _lambda.LayerVersion(self, "MyLayer3_10_2",
            code=_lambda.Code.from_asset("../lambdas/python.zip"),  # Asume que requirements.txt está en esta carpeta
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_10],
            layer_version_name="MyLayer"
        )

        # Crear la función Lambda
        lambda_fn = _lambda.Function(self, "ServerlessHandler",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset("../lambdas/src"),
            handler="handler.main",
            layers=[layer],  # Añadir la capa aquí
            environment={
                "TABLE_NAME": table.table_name,
            }
        )

        # permiso de lectura y escritura a la tabla 
        table.grant_read_write_data(lambda_fn)


        # Crear la API de API Gateway
        api = apigateway.RestApi(self, "candidatos-api",
            rest_api_name="Candidatos Service",
        )
        candidatos = api.root.add_resource("candidato")
        candidatos.add_method("POST", apigateway.LambdaIntegration(lambda_fn))

        # Crear alarma en CloudWatch
        alarm = cloudwatch.Alarm(self, "ErrorAlarm",
            metric=cloudwatch.Metric(
                metric_name="Errors",
                namespace="AWS/Lambda",
                dimensions_map={"FunctionName": lambda_fn.function_name},
                statistic="Sum",
                period=Duration.minutes(1),
            ),
            threshold=1,
            evaluation_periods=1,
        )

        # Crear tema SNS y subscripción por correo
        email_topic = sns.Topic(self, "LambdaAlertsTopic")
        email_topic.add_subscription(subscriptions.EmailSubscription("andresj15533@live.com"))

        # Agregar acción a la alarma
        alarm.add_alarm_action(cloudwatch_actions.SnsAction(email_topic))



        # Crear la función Lambda para enviar mensajes a Slack
        slack_lambda = _lambda.Function(self, "SendToSlackFunction",
        runtime=_lambda.Runtime.PYTHON_3_10,
        code=_lambda.Code.from_asset("../lambdas/src/slack"),
        handler="slack_notification.main",
        layers=[layer],
        environment={
            "SLACK_WEBHOOK_URL": "YOUR_SLACK_WEBHOOK_URL"  
        }
        )

        # Agregar la función Lambda como destino de la notificación de SNS
        slack_event_source = lambda_event_sources.SnsEventSource(email_topic)
        slack_lambda.add_event_source(slack_event_source)


