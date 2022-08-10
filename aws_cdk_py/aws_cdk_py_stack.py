from aws_cdk import (
    App,
    Stack
)


class AwsCdkPyStack(Stack):

    def __init__(self, app: App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        self.output_props = props.copy()

    # pass objects to another stack
    @property
    def outputs(self):
        return self.output_props
