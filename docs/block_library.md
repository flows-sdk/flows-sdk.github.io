# Block Library V32




## Blocks

### DB_ACCESS

name: Database Request

uuid: 3d2c7993-3096-4d83-884d-c447500dc063

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| db_type | string | "mssql" | Database type | N/A|
| host | string | N/A | Host/Server | URL/IP Address of the server DB is hosted on|
| port | integer | 1433 | Port | N/A|
| database | string | N/A | Database/Service | Database or Service name|
| username | string | N/A | Username | N/A|
| password | string | N/A | Password | N/A|
| options | object | {} | Additional Options | Dictionary of additional connection string options|
| timeout | integer | 120 | Timeout | Timeout in seconds|
| query | MultilineText | N/A | Query | Parameterized query|
| query_params | object | {} | Parameters | Dictionary of values for query placeholders|



### S3_DOWNLOADER

name: S3 Downloader

uuid: ed85bc11-eee0-4159-b66e-a3e67d5ef4a3

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| config | json | N/A |  | N/A|
| url | string | "" | URL | URL|
| endpoint_url | string | null | Endpoint URL | Endpoint URL|



### SOAP_REQ

name: SOAP API Request

uuid: 2c6aa317-2a06-44dd-af0c-08d8f4050129

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| endpoint | string | N/A | Endpoint URL | Absolute URL including schema to HTTP endpoint for this request.|
| method | string | "" | Method | SOAP Method to invoke|
| body_namespace | string | null | Body Namespace | SOAP request body namespace URI|
| headers_namespace | string | null | Headers Namespace | SOAP request headers namespace URI|
| headers | object | N/A | SOAP Headers | SOAP Headers|
| params | object | null | SOAP parameters | Key-value pair used as query parameters in the request to be inserted as soap body|



### HTTP_DOWNLOADER

name: HTTP Downloader

uuid: c7e1f048-f817-43fc-900b-6eabfa3dfb9a

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| headers | object | {} | URL Headers | N/A|
| url | string | "" | URL | URL|



### MANUAL_CLASSIFICATION_2

name: Manual Classification

uuid: 36f1316e-284c-482a-bf42-9ed4c5517f0d

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| layout_release_uuid | ReleaseUUID | N/A | Layout Release | N/A|
| manual_nlc_enabled | boolean | True | Manual Classification Supervision | Enables manual classification when applicable|
| submission | Submission | N/A | Submission Object | N/A|
| api_params | json | N/A | API Parameters | N/A|
| task_restrictions | TaskRestrictions | N/A | Default Task Restrictions | Defines what users can access Supervision tasks created by this block.|
| notification_workflow | string | "" | Notification Flow | Notification flow name to run when the submission enters Manual Classification|



### MACHINE_CLASSIFICATION_2

name: Machine Classification

uuid: 8a2d4c33-8e48-4192-b6a3-5194967e9501

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| layout_release_uuid | ReleaseUUID | N/A | Layout Release | N/A|
| submission | Submission | N/A | Submission Object | N/A|
| api_params | json | N/A | API Parameters | N/A|
| vpc_registration_threshold | number | 0.6 | Layout Variation Match Threshold | Structured pages above this threshold will be automatically matched to a layout variation.|
| nlc_enabled | boolean | True | Automatic Document Classification | Enables workflow to manage a model for automated classification of semi-structured and additional layout variations.|
| nlc_target_accuracy | Percentage | 0.99 | Classification Target Accuracy | N/A|
| nlc_doc_grouping_logic | string | N/A | Document Grouping Logic | Logic to handle multiple pages matched to the same layout variationin a given submission.|
| rotation_correction_enabled | boolean | True | Enabled | Identifies and corrects the orientation of semi-structured images.|
| mobile_processing_enabled | boolean | False | Enabled | Improves the machine readability of photo captured documents|



### MACHINE_TRANSCRIPTION_3

name: Machine Transcription

uuid: ca78dd22-d969-43c8-92ec-caae3321a7a4

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| layout_release_uuid | ReleaseUUID | N/A | Layout Release | N/A|
| submission | Submission | N/A | Submission Object | N/A|
| api_params | json | N/A | API Parameters | N/A|
| transcription_automation_training | boolean | True | Transcription Automation Training | N/A|
| transcription_model | string | N/A | Transcription Model Name | The transcription model that will be used for this flow|
| flex_confidence_boosting_enabled | boolean | False | Semi-structured confidence boosting | Boosts semi-structured transcription confidence for repeated values.|
| structured_text_target_accuracy | Percentage | 0.95 | Structured text target accuracy | N/A|
| structured_text_confidence_threshold | number | 0.52 | Default structured text threshold | N/A|
| structured_text_acceptable_confidence | number | 0.1 | Structured text minimum legibility threshold | N/A|
| semi_structured_text_target_accuracy | Percentage | 0.95 | Semi-structured text target accuracy | N/A|
| semi_structured_text_confidence_threshold | number | 0.52 | Default semi-structured text threshold | N/A|
| semi_structured_text_acceptable_confidence | number | 0.1 | Semi-structured text minimum legibility threshold | N/A|
| structured_checkbox_target_accuracy | Percentage | 0.95 | Structured checkbox target accuracy | N/A|
| structured_checkbox_confidence_threshold | number | 0.56 | Default structured checkbox threshold | N/A|
| structured_checkbox_acceptable_confidence | number | 0.5 | Structured checkbox minimum legibility threshold | N/A|
| structured_signature_target_accuracy | Percentage | 0.95 | Structured signature target accuracy | N/A|
| structured_signature_confidence_threshold | number | 0.99 | Default structured signature threshold | N/A|
| structured_signature_acceptable_confidence | number | 0.5 | Structured signature minimum legibility threshold | N/A|
| semi_structured_checkbox_target_accuracy | Percentage | 0.95 | Semi-structured checkbox target accuracy | N/A|
| semi_structured_checkbox_confidence_threshold | number | 0.56 | Default semi-structured checkbox threshold | N/A|
| semi_structured_checkbox_acceptable_confidence | number | 0.5 | Semi-structured checkbox minimum legibility threshold | N/A|
| finetuning_only_trained_layouts | boolean | False | Run finetuning only for trained layouts | N/A|



### MANUAL_TRANSCRIPTION_2

name: Manual Transcription

uuid: 61b64899-9ea5-4911-81c5-764b24fb0f4d

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| submission | Submission | N/A | Submission Object | N/A|
| api_params | json | N/A | API Parameters | N/A|
| task_restrictions | TaskRestrictions | N/A | Default Task Restrictions | Defines what users can access Supervision tasks for submission from a particular source or submissions matching a specific layout.|
| manual_transcription_enabled | boolean | True | Manual Transcription Supervision | Enables manual transcription when applicable.|
| supervision_transcription_masking | boolean | True | Supervision Transcription Masking | Prevents users from inputting invalid characters during Supervision Transcription tasks.|
| table_output_manual_review | boolean | False | Table Output Manual Review | Always generates a table transcription task if the layout contains a table. If disabled, a table transcription task will only be generated if one or more cells have transcribed values below the defined thresholds.|
| always_supervise_blank_cells | boolean | True | Send Blank Cells to Manual Transcription | If enabled, always send blank cells in transcribed tables to be supervised manually, regardless of confidence.|
| notification_workflow | string | "" | Notification Flow | Notification flow name to run when the submission enters Manual Transcription|



### SEGMENT_AND_OICR_2

name: Segmentation and Full Page OICR

uuid: c00417d3-7955-42bb-99de-10d25ad72b6a

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| app_metadata | array | N/A | App Metadata | N/A|
| rotation_correction_enabled | boolean | True | Rotation Correction Enabled | N/A|
| mobile_processing_enabled | boolean | False | Captured Image Enhancement | N/A|
| page | Page | N/A | Page Object | N/A|



### SUBMISSION_COMPLETE_3

name: Complete

uuid: cf0d8e8e-b736-46aa-bef1-5f4447a2d505

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| submission | Submission | N/A | Submission Object | N/A|
| payload | json | N/A | Transformed Output | N/A|
| nlc_qa_sampling_ratio | Percentage | 0.05 | QA sample rate | Defines the percentage of documents sampled for Classification QA.|
| field_id_qa_enabled | boolean | True | Quality Assurance | N/A|
| field_id_qa_sampling_ratio | Percentage | 0.05 | QA sample rate | Defines the percentage of documents sampled for Identification QA.|
| table_id_qa_enabled | boolean | True | TABLE IDENTIFICATION QUALITY ASSURANCE | Allows users to verify the location of table cells.|
| table_id_qa_sampling_ratio | Percentage | 0.05 | TABLE IDENTIFICATION QA SAMPLE RATE | Defines the percentage of tables the system samples for QA.|
| transcription_qa_enabled | boolean | True | Quality Assurance | N/A|
| transcription_qa_sampling_ratio | Percentage | 0.05 | QA sample rate | Defines the percentage of fields sampled for Transcription QA.|
| table_cell_transcription_qa_enabled | boolean | True | Table Transcription Quality Assurance | N/A|
| table_cell_transcription_qa_sample_rate | Percentage | 0.05 | Table Transcription QA Sample Rate | Defines the percentage of cells the system samples for QA. This value is likely to be lower than "Transcription QA Sample Rate" since there are more table cells than fields on any given page.|



### MACHINE_IDENTIFICATION_3

name: Machine Identification

uuid: 7ea6fcc1-47ac-406d-b82c-e72371e6eda6

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| submission | Submission | N/A | Submission Object | Submission object|
| api_params | json | N/A | API Parameters | N/A|
| field_id_target_accuracy | Percentage | 0.95 | Field ID Target Accuracy | Field ID Target Accuracy|
| table_id_target_accuracy | Percentage | 0.96 | Table ID Target Accuracy | Table ID Target Accuracy|
| manual_field_id_enabled | boolean | True | Manual Field Identification Supervision | Enables manual identification when applicable|



### MANUAL_IDENTIFICATION_3

name: Manual Identification

uuid: 0eab3750-0abb-4d02-a585-7e7e43e9cffe

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| submission | Submission | N/A | Submission Object | Submission object|
| layout_release_uuid | ReleaseUUID | N/A | Layout Release UUID | Layout Release UUID|
| api_params | json | N/A | API Parameters | N/A|
| task_restrictions | TaskRestrictions | N/A | Default Task Restrictions | Defines what users can access Supervision tasks created by this block|
| manual_field_id_enabled | boolean | True | Manual Field Identification Supervision | Enables manual identification when applicable|
| notification_workflow | string | "" | Notification Flow | Notification flow name to run when the submission enters Manual Identification|



### SUBMISSION_BOOTSTRAP_2

name: Submission Initialization

uuid: f0028612-775c-42b3-92df-848db8c8d530


.. automodule:: flows_sdk.examples.idp_v32_starter.idp_blocks:SubmissionBootstrapV2Block
   :members:
   :undoc-members:
   :show-inheritance:

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| $trigger | object | N/A | Trigger | Trigger|
| workflow_uuid | uuid | N/A | Workflow Version UUID | UUID of the triggered workflow version|
| workflow_name | string | N/A | Workflow name | Name of the triggered workflow|
| workflow_version | integer | N/A | Workflow version | Version of the triggered workflow|
| s3_config | object | N/A | S3 Submission Retrieval Store | Specify Amazon S3 credentials for submission retrieval store. Expects a json expression: {"aws_access_key_id": "X", "aws_secret_access_key": "Y"}|
| s3_endpoint_url | string | N/A | S3 Submission Retrieval Endpoint URL | Endpoint URL for S3 submission retrieval store|
| ocs_config | object | N/A | OCS Configuration | OCS Configuration for downloading submission data|
| layout_release_uuid | uuid | N/A | Layout Release UUID | Layout Release UUID at submission creation time|
| notification_workflow | string | "" | Notification Flow | Notification flow name to run when the submission is initialized|



### FLEXIBLE_EXTRACTION

name: Flexible Extraction

uuid: efda60f7-4150-4164-b191-312ad1512314

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| layout_release_uuid | ReleaseUUID | N/A | Layout Release UUID | Layout Release UUID|
| submission | Submission | N/A | Submission Object | N/A|
| api_params | json | N/A | API Parameters | N/A|
| task_restrictions | TaskRestrictions | N/A | Default Task Restrictions | Defines what users can access Supervision tasks created by this block.|
| supervision_transcription_masking | boolean | True | Flexible Extraction Transcription Masking | Prevents users from inputting invalid characters during the Flexible Extraction task.|
| notification_workflow | string | "" | Notification Flow | Notification flow name to run when the submission enters Flexible Extraction|



### MACHINE_COLLATION_2

name: Machine Collation

uuid: d21063fa-f79d-4b55-a48a-801b61a9e270

Inputs:

| name | type | default value | title | description |
| ---  | ---  | ---           | ---   | ---         |
| submission | Submission | N/A | Submission Object | Submission object|
| cases | array | N/A | Cases information | This parameter accepts an array of JSON objects that contain information on how Cases should be created. There are two ways to collate a case: by the filenames specified in the current Submission, or by the ids of the Documents or Pages submitted in previous submissions.|
| dedupe_files | boolean | False | Replace case data from duplicate file names | Enabling this setting will replace case data from repeated file names within the same case. Cases will retain data from the most recently submitted version of a particular file. Note that this setting does not delete the old data, it just removes it from the case|


