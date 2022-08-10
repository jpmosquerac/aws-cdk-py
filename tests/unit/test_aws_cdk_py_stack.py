import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_py.aws_cdk_py_stack import AwsCdkPyStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_cdk_py/aws_cdk_py_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsCdkPyStack(app, "aws-cdk-py")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
