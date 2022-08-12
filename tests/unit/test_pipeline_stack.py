import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_py.pipeline_stack import Pipeline

def test_backend_stack():
    app = core.App()
    stack = Pipeline(app, "aws-cdk-py")
    template = assertions.Template.from_stack(stack)

    template.has_resource('AWS::Lambda::Function')
    template.has_resource('AWS::ApiGateway::RestApi')
    template.has_resource('AWS::DynamoDB::Table')