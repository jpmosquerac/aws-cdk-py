from aws_cdk import (
    App,
    assertions
)

from aws_cdk_py.pipeline_stack import Pipeline

def test_backend_stack():
    app = App()
    stack = Pipeline(app, "aws-cdk-py")
    template = assertions.Template.from_stack(stack)

    template.has_resource('')