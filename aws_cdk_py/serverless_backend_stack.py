import os

from aws_cdk import (
    Aws, App,
    Stack, 
    aws_s3,
    aws_lambda,
    aws_dynamodb,
    RemovalPolicy,
    aws_apigateway,
)

class ServerlessBackendStack(Stack):

    def __init__(self, app: App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        lambda_ = aws_lambda.Function(self, id='lambdafunction', function_name="lambdafunction", runtime=aws_lambda.Runtime.PYTHON_3_7,
                                     handler='index.handler',
                                     code=aws_lambda.Code.from_asset(
                                         os.path.join("./", "lambda-handler")),
                                     )

        api = aws_apigateway.LambdaRestApi(
            self, id='lambdaapi', rest_api_name='lambdaapi', handler=lambda_, proxy=True)

        postData = api.root.add_resource("sum")
        
        postData.add_method("POST")

        self.output_props = props.copy()
        self.output_props['lambda'] = lambda_

    @property
    def outputs(self):
        return self.output_props