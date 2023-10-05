import aws_cdk as core
import aws_cdk.assertions as assertions

from src.experimento1_stack import Experimento1Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in experimento1/experimento1_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Experimento1Stack(app, "experimento1")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
