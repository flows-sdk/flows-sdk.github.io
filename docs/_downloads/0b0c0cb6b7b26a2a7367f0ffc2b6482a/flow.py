from typing import Any
from uuid import UUID

from flows_sdk.blocks import CodeBlock
from flows_sdk.implementations.idp_v32.idp_blocks import (
    CaseCollationBlock,
    FlexibleExtractionBlock,
    IDPOutputsBlock,
    MachineClassificationBlock,
    MachineIdentificationBlock,
    MachineTranscriptionBlock,
    ManualClassificationBlock,
    ManualIdentificationBlock,
    ManualTranscriptionBlock,
    SubmissionBootstrapBlock,
    SubmissionCompleteBlock,
)
from flows_sdk.implementations.idp_v32.idp_values import (
    IDPManifest,
    IDPTriggers,
    get_idp_wf_config,
    get_idp_wf_inputs,
)
from flows_sdk.flows import Flow
from flows_sdk.package_utils import export_flow


def entry_point_flow() -> Flow:
    return idp_workflow()


def idp_workflow() -> Flow:
    idp_wf_config = get_idp_wf_config()

    # The idp flow basically processes, modifies and propagates the submission object from
    # block to block
    # Each block's processing result is usually included in the submission object

    # Submission bootstrap block initializes the submission object and prepares external images
    # or other submission data if needed
    submission_bootstrap = SubmissionBootstrapBlock(reference_name='submission_bootstrap')

    # Case collation block groups files, documents and pages (from the submission) into cases
    # In this example, case collation block receives the submission object and the cases
    # information from submission bootstrap block
    case_collation = CaseCollationBlock(
        reference_name='machine_collation',
        submission=submission_bootstrap.output('result.submission'),
        cases=submission_bootstrap.output('result.api_params.cases'),
    )

    # Machine classification block automatically matches documents to structured, semi-structured
    # or additional layouts
    # In this example, machine classification block receives the submission object from
    # case collation block
    machine_classification = MachineClassificationBlock(
        reference_name='machine_classification',
        submission=case_collation.output('submission'),
        api_params=submission_bootstrap.output('result.api_params'),
        # api_params is some submission processing settings obtained from submission bootstrap
        # that users do not have to worry about
    )

    # Manual classification block allows keyers to manually match submissions to their layouts.
    # Keyers may perform manual classification if machine classification cannot automatically
    # match a submission to a layout with high confidence
    # In this example, manual classification block receives the submission object from machine
    # classification block
    manual_classification = ManualClassificationBlock(
        reference_name='manual_classification',
        submission=machine_classification.output('submission'),
        api_params=submission_bootstrap.output('result.api_params'),
        # api_params is some submission processing settings obtained from submission bootstrap
        # that users do not have to worry about
    )

    # Machine identification automatically identify fields and tables in the submission
    # In this example, machine identification block receives the submission object from manual
    # classification
    machine_identification = MachineIdentificationBlock(
        reference_name='machine_identification',
        submission=manual_classification.output('submission'),
        api_params=submission_bootstrap.output('result.api_params'),
        # api_params is some submission processing settings obtained from submission bootstrap
        # that users do not have to worry about
    )

    # Manual identification allows keyers to complete field identification or table identification
    # tasks, where they draw bounding boxes around the contents of certain fields, table columns
    # or table rows. This identification process ensures that the system will be able to
    # transcribe the correct content in the upcoming transcription process
    # In this example, manual identification block receives the submission object from machine
    # identification
    manual_identification = ManualIdentificationBlock(
        reference_name='manual_identification',
        submission=machine_identification.output('submission'),
        api_params=submission_bootstrap.output('result.api_params'),
        # api_params is some submission processing settings obtained from submission bootstrap
        # that users do not have to worry about
    )

    # Machine transcription automatically transcribes the content of your submission
    # In this example, machine identification block receives the submission object from manual
    # identification
    machine_transcription = MachineTranscriptionBlock(
        reference_name='machine_transcription',
        submission=manual_identification.output('submission'),
        api_params=submission_bootstrap.output('result.api_params'),
        # api_params is some submission processing settings obtained from submission bootstrap
        # that users do not have to worry about
    )

    # Manual transcription lets your keyers manually enter the text found in fields or tables
    # that could not be automatically transcribed
    # In this example, manual transcription block receives the submission object from machine
    # transcription block
    manual_transcription = ManualTranscriptionBlock(
        reference_name='manual_transcription',
        submission=machine_transcription.output('submission'),
        api_params=submission_bootstrap.output('result.api_params'),
        # api_params is some submission processing settings obtained from submission bootstrap
        # that users do not have to worry about
    )

    # Flexible extraction manually transcribes fields marked for review
    # In this example, flexible extraction block receives the submission object from manual
    # transcription block
    flexible_extraction = FlexibleExtractionBlock(
        reference_name='flexible_extraction',
        submission=manual_transcription.output('submission'),
        api_params=submission_bootstrap.output('result.api_params'),
        # api_params is some submission processing settings obtained from submission bootstrap
        # that users do not have to worry about
    )

    def _mark_as_completed(submission: Any) -> Any:
        from datetime import datetime

        dt_completed = datetime.isoformat(datetime.utcnow())
        dt_completed_fmt = dt_completed + 'Z'

        for document in submission['documents']:
            document['state'] = 'complete'
            document['complete_time'] = dt_completed_fmt

            for page in document['pages']:
                page['state'] = 'complete'

        for page in submission['unassigned_pages']:
            page['state'] = 'complete'

        submission['state'] = 'complete'
        submission['complete_time'] = dt_completed_fmt

        return submission

    # Custom code block enables users to transform and validate extracted submission data
    # before Hyperscience sends it to downstream systems
    # In this example, user created a _mark_as_completed function to transform and validate
    # submission data
    # Notice that the _mark_as_completed function takes in a single argument which is passed
    # in using the code_input parameter
    custom_code = CodeBlock(
        reference_name='mark_as_completed',
        code=_mark_as_completed,
        code_input={'submission': flexible_extraction.output('submission')},
        title='Mark As Completed',
        description='Updated Transformed JSON to Completed State',
    )

    # Submission complete block finalizes submission processing and updates reporting data
    # Every flow needs a complete block because it initiates Quality Assurance tasks and
    # changes the submission's status to "Complete"
    # In this example, submission complete block receives the submission object from
    # marked_as_complete custom code block
    submission_complete = SubmissionCompleteBlock(
        reference_name='complete_submission', submission=custom_code.output('submission')
    )

    # Output block allows users to send data extracted by this idp flow to other systems
    # for downstream processing
    # In this example, no output block is instantiated (blocks=[])
    # Setting up output blocks via UI and leaving this empty is recommended
    outputs = IDPOutputsBlock(
        inputs={'submission': submission_bootstrap.output('result.submission')}, blocks=[]
    )

    # Trigger block allows users to send data to idp flow via sources other than the User Interface
    # In this example, no trigger block is instantiated (blocks=[])
    # Setting up trigger blocks via UI and leaving this empty is recommended
    triggers = IDPTriggers(blocks=[])

    return Flow(
        # Flows should have a deterministic UUID ensuring cross-system consistency
        uuid=UUID('f923871d-8742-45cd-ae6d-e0429c098421'),
        owner_email='harry.yu@hyperscience.com',
        title='IDP with Custom Code Block Flow Example (V32)',
        # Flow identifiers are globally unique
        manifest=IDPManifest(flow_identifier='IDP_WITH_CUSTOM_CODE_V32_FLOW_EXAMPLE'),
        triggers=triggers,
        # It is important to include all blocks that are instantiated here in the blocks
        # field and make sure they follow the order of the flow. For example, if machine
        # classification depends on the output of case collation, then case_collation must
        # come before machine_classification in this blocks array
        blocks=[
            submission_bootstrap,
            case_collation,
            machine_classification,
            manual_classification,
            machine_identification,
            manual_identification,
            machine_transcription,
            manual_transcription,
            flexible_extraction,
            custom_code,
            submission_complete,
            outputs,
        ],
        input=get_idp_wf_inputs(idp_wf_config),
        description='Intelligent Document Processing with Custom Code Block Flow Example (V32)',
        output={'submission': submission_complete.output()},
    )


if __name__ == '__main__':
    export_flow(flow=entry_point_flow())
