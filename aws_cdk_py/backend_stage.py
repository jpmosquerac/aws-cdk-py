from aws_cdk import (
    App, Stage
)

from aws_cdk_py.serverless_backend_stack import ServerlessBackendStack

class ServerlessBackendStage(Stage):
    def __init__(self, app: App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        serverlessBackendStack = ServerlessBackendStack(self, f"{props['namespace']}-ServerlessBackendStack", props)