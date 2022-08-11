import os

from aws_cdk import (
    Aws, App,
    Stack, 
    aws_s3,
    aws_lambda,
    aws_cognito,
    aws_dynamodb,
    RemovalPolicy,
    aws_apigateway,
)

class ServerlessBackendStack(Stack):

    def __init__(self, app: App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        bucket = aws_s3.Bucket(
            self, 'ProjectBucket',
            bucket_name=f"{props['namespace'].lower()}-{Aws.ACCOUNT_ID}",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        user_pool = aws_cognito.UserPool(self, "UserPool")

        user_pool.add_client("app-client", auth_flows=aws_cognito.AuthFlow(
            user_password=True
        ),
            supported_identity_providers=[
                aws_cognito.UserPoolClientIdentityProvider.COGNITO]
        )

        auth = aws_apigateway.CognitoUserPoolsAuthorizer(self, "imagesAuthorizer",
                                                      cognito_user_pools=[
                                                          user_pool]
                                                      )

        table = aws_dynamodb.Table(self, id='dynamoTable', table_name='formmetadata', partition_key=aws_dynamodb.Attribute(
            name='userid', type=aws_dynamodb.AttributeType.STRING)) #change primary key here

        lambda_ = aws_lambda.Function(self, id='lambdafunction', function_name="formlambda", runtime=aws_lambda.Runtime.PYTHON_3_7,
                                     handler='index.handler',
                                     code=aws_lambda.Code.from_asset(
                                         os.path.join("./", "lambda-handler")),
                                     environment={
                                         'bucket': bucket.bucket_name,
                                         'table': table.table_name
                                     }
                                     )

        bucket.grant_read_write(lambda_)

        table.grant_read_write_data(lambda_)

        api = aws_apigateway.LambdaRestApi(
            self, id='lambdaapi', rest_api_name='formapi', handler=lambda_, proxy=True)

        postData = api.root.add_resource("form")
        
        postData.add_method("POST", authorizer=auth,
                          authorization_type=aws_apigateway.AuthorizationType.COGNITO)  # POST images/files & metadata

        self.output_props = props.copy()
        self.output_props['bucket'] = bucket
        self.output_props['lambda'] = lambda_

    @property
    def outputs(self):
        return self.output_props