import os

from aws_cdk import (
    App,
    RemovalPolicy,
    Stack, 
    aws_lambda,
    aws_dynamodb,
    aws_apigateway,
    aws_s3
)

class BackendStack(Stack):

    def __init__(self, app: App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        bucket =  aws_s3.Bucket(self, id='s3bucket',
                               bucket_name='testbucketJP1234', removal_policy=RemovalPolicy.DESTROY)

        table = aws_dynamodb.Table(self, id='dynamoTable', table_name='backendtable', 
                                removal_policy=RemovalPolicy.DESTROY,
                                partition_key=aws_dynamodb.Attribute(name='id', type=aws_dynamodb.AttributeType.STRING)) #change primary key here

        lambda_ = aws_lambda.Function(self, id='lambdafunction', function_name="backendfunction", 
                                    runtime=aws_lambda.Runtime.PYTHON_3_7,
                                    handler='index.handler',
                                    code=aws_lambda.Code.from_asset(
                                    os.path.join("./", "lambda-handler")),
                                    environment={
                                        'table': table.table_name
                                    })
        
        table.grant_read_write_data(lambda_)

        api = aws_apigateway.LambdaRestApi(
            self, id='lambdaapi', rest_api_name='lambdaapi', handler=lambda_, proxy=False)

        postData = api.root.add_resource("api")
        
        postData.add_method("POST")

        self.output_props = props.copy()
        self.output_props['table'] = table
        self.output_props['lambda'] = lambda_
        self.output_props['api'] = api

    @property
    def outputs(self):
        return self.output_props