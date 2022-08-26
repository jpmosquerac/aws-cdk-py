from aws_cdk import (
    App, Stage
)

from aws_cdk_py.frontend_stack import FrontendStack

class FrontendStage(Stage):
    def __init__(self, app: App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        frontendStack = FrontendStack(self, f"{props['namespace']}-FrontendStack", props)