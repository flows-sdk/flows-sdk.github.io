from uuid import UUID

from flows_sdk.implementations.idp_v32.idp_blocks import (
    CaseCollation,
    FlexibleExtraction,
    IDPOutputs,
    MachineClassification,
    MachineIdentification,
    MachineTranscription,
    ManualClassification,
    ManualIdentification,
    ManualTranscription,
    SubmissionBootstrap,
    SubmissionComplete,
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
    submission_bootstrap = SubmissionBootstrap(reference_name='submission_bootstrap')

    # Case collation block groups files, documents and pages (from the submission) into cases
    # In this example, case collation block receives the submission object and the cases
    # information from submission bootstrap block
    case_collation = CaseCollation(
        reference_name='machine_collation',
        submission=submission_bootstrap.output('result.submission'),
        cases=submission_bootstrap.output('result.api_params.cases'),
    )

    # Machine classification block automatically matches documents to structured, semi-structured
    # or additional layouts
    # In this example, machine classification block receives the submission object from
    # case collation block
    machine_classification = MachineClassification(
        reference_name='machine_classification',
        submission=case_collation.output('submission'),
        api_params=submission_bootstrap.output('result.api_params'),
        rotation_correction_enabled=idp_wf_config.rotation_correction_enabled,
    )

    # Manual classification block allows keyers to manually match submissions to their layouts.
    # Keyers may perform manual classification if machine classification cannot automatically
    # match a submission to a layout with high confidence
    # In this example, manual classification block receives the submission object from machine
    # classification block
    manual_classification = ManualClassification(
        reference_name='manual_classification',
        submission=machine_classification.output('submission'),
        api_params=submission_bootstrap.output('result.api_params'),
    )

    # Machine identification automatically identify fields and tables in the submission
    # In this example, machine identification block receives the submission object from manual
    # classification
    machine_identification = MachineIdentification(
        reference_name='machine_identification',
        submission=manual_classification.output('submission'),
        api_params=submission_bootstrap.output('result.api_params'),
    )

    # Manual identification allows keyers to complete field identification or table identification
    # tasks, where they draw bounding boxes around the contents of certain fields, table columns
    # or table rows. This identification process ensures that the system will be able to
    # transcribe the correct content in the upcoming transcription process
    # In this example, manual identification block receives the submission object from machine
    # identification
    manual_identification = ManualIdentification(
        reference_name='manual_identification',
        submission=machine_identification.output('submission'),
        api_params=submission_bootstrap.output('result.api_params'),
        task_restrictions=idp_wf_config.manual_identification_config.task_restrictions,
    )

    # Machine transcription automatically transcribes the content of your submission
    # In this example, machine identification block receives the submission object from manual
    # identification
    machine_transcription = MachineTranscription(
        reference_name='machine_transcription',
        submission=manual_identification.output('submission'),
        api_params=submission_bootstrap.output('result.api_params'),
    )

    # Manual transcription lets your keyers manually enter the text found in fields or tables
    # that could not be automatically transcribed
    # In this example, manual transcription block receives the submission object from machine
    # transcription block
    manual_transcription = ManualTranscription(
        reference_name='manual_transcription',
        submission=machine_transcription.output('submission'),
        api_params=submission_bootstrap.output('result.api_params'),
        supervision_transcription_masking=(
            idp_wf_config.manual_transcription_config.supervision_transcription_masking
        ),
        table_output_manual_review=(
            idp_wf_config.manual_transcription_config.table_output_manual_review
        ),
        task_restrictions=idp_wf_config.manual_transcription_config.task_restrictions,
    )

    # Flexible extraction manually transcribes fields marked for review
    # In this example, flexible extraction block receives the submission object from manual
    # transcription block
    flexible_extraction = FlexibleExtraction(
        reference_name='flexible_extraction',
        submission=manual_transcription.output('submission'),
        api_params=submission_bootstrap.output('result.api_params'),
        supervision_transcription_masking=(
            idp_wf_config.flexible_extraction_config.supervision_transcription_masking
        ),
        task_restrictions=idp_wf_config.flexible_extraction_config.task_restrictions,
    )

    # Submission complete block finalizes submission processing and updates reporting data
    # Every flow needs a complete block because it initiates Quality Assurance tasks and
    # changes the submission's status to "Complete"
    # In this example, submission complete block receives the submission object from
    # marked_as_complete custom code block
    submission_complete = SubmissionComplete(
        reference_name='complete_submission', submission=flexible_extraction.output('submission')
    )

    # Output block allows users to send data extracted by this idp flow to other systems
    # for downstream processing
    # In this example, this is an empty output block that does not do anything by default
    outputs = IDPOutputs(inputs={'submission': submission_bootstrap.output('result.submission')})

    return Flow(
        # Flows should have a deterministic UUID ensuring cross-system consistency
        uuid=UUID('5d1515a9-ae37-45fc-bb03-d7dda943b60d'),
        owner_email='harry.yu@hyperscience.com',
        title='IDP Flow Example (V32)',
        # Flow identifiers are globally unique
        manifest=IDPManifest(flow_identifier='IDP_V32_FLOW_EXAMPLE'),
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
            submission_complete,
            outputs,
        ],
        input=get_idp_wf_inputs(idp_wf_config),
        description='Intelligent Document Processing Flow Example (V32)',
        triggers=IDPTriggers(),
        output={'submission': submission_complete.output()},
    )


if __name__ == '__main__':
    export_flow(flow=entry_point_flow())
