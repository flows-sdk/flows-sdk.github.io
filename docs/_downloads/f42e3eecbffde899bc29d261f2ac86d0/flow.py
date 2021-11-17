from uuid import UUID

from flows_sdk import utils
from flows_sdk.blocks import CodeBlock
from flows_sdk.flows import Flow, Manifest, Parameter
from flows_sdk.package_utils import export_flow

# Flow identifiers are globally unique
# New versions in case of backward incompatibility are expected to have a different name
# (e.g. HELLO_FLOW_2).
# By convention, identifiers are snake-cased capital letter strings with an optional numeric suffix.
HELLO_FLOW_IDENTIFIER = 'HELLO_FLOW'

# Flows should have a deterministic UUID ensuring cross-system consistency
HELLO_FLOW_UUID = UUID('2e3ab564-fcf5-41fb-a573-4bc2fd153b6d')


def entry_point_flow() -> Flow:
    return sample_flow_with_secret()


# Flow inputs can be referenced in blocks, so usually it is a good idea define them somewhere
class FlowInputs:
    HELLO_INPUT = 'hello_input'


def sample_flow_with_secret() -> Flow:
    def code_fn(code_block_input_param: str) -> str:
        return f'Hello {code_block_input_param}'

    # Parameters can be added to a :func:`~Flow`
    hello_input_param = Parameter(
        name=FlowInputs.HELLO_INPUT, title='Hello input', type='string', optional=False
    )

    ccb = CodeBlock(
        reference_name='hello_ccb',
        code=code_fn,
        code_input={'code_block_input_param': utils.workflow_input(FlowInputs.HELLO_INPUT)},
    )

    return Flow(
        depedencies={},
        title='Hello World Flow',
        description='A simple Flow showcasing how inputs are passed',
        blocks=[ccb],
        owner_email='viktor.penelski@hyperscience.com',
        manifest=Manifest(identifier=HELLO_FLOW_IDENTIFIER, input=[hello_input_param]),
        uuid=HELLO_FLOW_UUID,
        input={FlowInputs.HELLO_INPUT: 'World'},
    )


if __name__ == '__main__':
    export_flow(flow=entry_point_flow())
