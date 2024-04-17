import aws_cdk as core
from aws_cdk import aws_lambda as lambda_
import aws_cdk.aws_apigatewayv2 as apigw
from aws_cdk import aws_iam as iam
from aws_cdk.aws_apigatewayv2_integrations import WebSocketLambdaIntegration
from constructs import Construct

class WebsocketPocStack(core.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Crear la función Lambda
        lambda_function = lambda_.Function(
            self, 'WebSocketHandler',
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler='ws_function.handler',
            code=lambda_.Code.from_asset('./lambda'),
            timeout=core.Duration.seconds(10)
        )

        lambda_function.add_to_role_policy(iam.PolicyStatement(
            actions=["execute-api:ManageConnections"],
            resources=["*"],#arn:aws:execute-api:REGION:ACCOUNT-ID:API-ID/STAGE-NAME/*
            effect=iam.Effect.ALLOW
        ))

        # Crear la API WebSocket
        api = apigw.WebSocketApi(self, "WebsocketApi")
        '''api = apigw.WebSocketApi(
            self, 'WebsocketApi',
            connect_route_options=apigw.WebSocketRouteOptions(
                integration=apigw.LambdaWebSocketIntegration(handler=lambda_function),
            ),
            disconnect_route_options=apigw.WebSocketRouteOptions(
                integration=apigw.LambdaWebSocketIntegration(handler=lambda_function),
            ),
            default_route_options=apigw.WebSocketRouteOptions(
                integration=apigw.LambdaWebSocketIntegration(handler=lambda_function),
            )
        )'''

        # Despliegue de la API
        stage = apigw.WebSocketStage(
            self, 'DevStage',
            web_socket_api=api,
            stage_name='dev',
            auto_deploy=True
        )

        api.add_route("sendMessage",
            integration=WebSocketLambdaIntegration("SendMessageIntegration", lambda_function)
        )
        # Mostrar la URL de conexión WebSocket en la salida
        core.CfnOutput(self, "WebSocketURL", value=stage.url)
