from aws_cdk import (
    App, Stage
)

from aws_cdk_py.backend_stack import BackendStack

class BackendStage(Stage):
    def __init__(self, app: App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        backendStack = BackendStack(self, f"{props['namespace']}-BackendStack", props)