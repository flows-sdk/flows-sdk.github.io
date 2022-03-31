from uuid import UUID

from flows_sdk.flows import Flow, Manifest
from flows_sdk.implementations.idp_v32.idp_blocks import (
    IDPFullPageTranscriptionBlock,
    IDPImageCorrectionBlock,
    IDPOutputsBlock,
    SubmissionBootstrapBlock,
    SubmissionCompleteBlock,
)
from flows_sdk.implementations.idp_v32.idp_values import IDPTriggers
from flows_sdk.package_utils import export_flow


def entry_point_flow() -> Flow:
    return idp_fpt_workflow()


def idp_fpt_workflow() -> Flow:
    # The idp flow basically processes, modifies and propagates the submission object from
    # block to block
    # Each block's processing result is usually included in the submission object

    # Submission bootstrap block initializes the submission object and prepares external images
    # or other submission data if needed
    submission_bootstrap = SubmissionBootstrapBlock(reference_name='submission_bootstrap')

    image_correction = IDPImageCorrectionBlock(
        reference_name='image_correction', submission=submission_bootstrap.output('submission')
    )

    full_page_transcription = IDPFullPageTranscriptionBlock(
        reference_name='full_page_transcription', submission=image_correction.output('submission')
    )

    # Submission complete block finalizes submission processing and updates reporting data
    # Every flow needs a complete block because it initiates Quality Assurance tasks and
    # changes the submission's status to "Complete"
    # In this example, submission complete block receives the submission object from
    # marked_as_complete custom code block
    submission_complete = SubmissionCompleteBlock(
        reference_name='complete_submission',
        payload=full_page_transcription.output('submission'),
        submission=full_page_transcription.output('submission'),
        nlc_qa_sampling_ratio=0,
        field_id_qa_enabled=False,
        field_id_qa_sampling_ratio=0,
        table_id_qa_enabled=False,
        table_id_qa_sampling_ratio=0,
        transcription_qa_enabled=False,
        transcription_qa_sampling_ratio=0,
        table_cell_transcription_qa_enabled=False,
        table_cell_transcription_qa_sample_rate=0,
    )

    # Output block allows users to send data extracted by this idp flow to other systems
    # for downstream processing
    # In this example, no output block is instantiated (blocks=[])
    # Setting up output blocks via UI and leaving this empty is recommended
    outputs = IDPOutputsBlock(
        inputs={'submission': submission_bootstrap.output('submission')}, blocks=[]
    )

    # Trigger block allows users to send data to idp flow via sources other than the User Interface
    # In this example, no trigger block is instantiated (blocks=[])
    # Setting up trigger blocks via UI and leaving this empty is recommended
    triggers = IDPTriggers(blocks=[])

    return Flow(
        # Flows should have a deterministic UUID ensuring cross-system consistency
        uuid=UUID('0dd837ae-44da-425a-b4be-9ffa3fc40eab'),
        owner_email='harry.yu@hyperscience.com',
        title='IDP Full Page Transcription Flow Example (V32)',
        # Flow identifiers are globally unique
        manifest=Manifest(identifier='IDP_FULL_PAGE_TRANSCRIPTION_V32_FLOW_EXAMPLE', input=[]),
        triggers=triggers,
        # It is important to include all blocks that are instantiated here in the blocks
        # field and make sure they follow the order of the flow. For example, if machine
        # classification depends on the output of case collation, then case_collation must
        # come before machine_classification in this blocks array
        blocks=[
            submission_bootstrap,
            image_correction,
            full_page_transcription,
            submission_complete,
            outputs,
        ],
        description='IDP Full Page Transcription Flow Example (V32)',
        output={'submission': submission_complete.output()},
    )


if __name__ == '__main__':
    export_flow(flow=entry_point_flow())
