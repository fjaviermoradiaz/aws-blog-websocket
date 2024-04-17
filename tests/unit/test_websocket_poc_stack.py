import aws_cdk as core
import aws_cdk.assertions as assertions

from websocket_poc.websocket_poc_stack import WebsocketPocStack

# example tests. To run these tests, uncomment this file along with the example
# resource in websocket_poc/websocket_poc_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = WebsocketPocStack(app, "websocket-poc")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
