"""
Constant variables related to creating a yaml file from a google spreadsheet.
"""

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
]

NEWLINE = ' <NEWLINE> '

# Special Field identifiers
CONCEPT_ID_FIELD = 'concept_id'
GENERALIZED_CONCEPT_ID_FIELD = 'generalized_output_concept_id'
INPUT_CONCEPT_ID_FIELD = 'input_concept_id'
VERSION = 'version'
REGISTERED_TRANSFORM_FIELD = 'transformed_by_registered_tier_privacy_methods'
DATE_REQUESTED_FIELD = 'date_requested'
DATE_COMPLETED_FIELD = 'date_completed'
CREATED_TIME_FIELD = 'created_time'
MODIFIED_TIME_FIELD = 'modified_time'
AFFECTED_BY_PRIVACY_METHODOLOGY_FIELD = 'affected_by_privacy_methodology'

INTEGER_FIELDS = [
    CONCEPT_ID_FIELD,
    GENERALIZED_CONCEPT_ID_FIELD,
    VERSION,
]

BOOLEAN_FIELDS = [
    REGISTERED_TRANSFORM_FIELD,
    AFFECTED_BY_PRIVACY_METHODOLOGY_FIELD,
]

TEMPORAL_FIELDS = [
    DATE_REQUESTED_FIELD,
    DATE_COMPLETED_FIELD,
    CREATED_TIME_FIELD,
    MODIFIED_TIME_FIELD,
]

MULTIPLE_TYPES = [
    INPUT_CONCEPT_ID_FIELD,
]

CHANGE_LOG_TAB_NAME = 'Change Log'
AVAILABLE_FIELDS_TAB_NAME = 'Available Fields'
TABLE_SUPPRESSIONS_TAB_NAME = 'Table Suppressions'
FIELD_SUPPRESSIONS_TAB_NAME = 'Field (Column) Suppressions'
CONCEPT_SUPPRESSIONS_TAB_NAME = 'Concept (Row) Suppressions'
FIELD_GENERALIZATIONS_TAB_NAME = 'Field (Column) Generalizations'
CONCEPT_GENERALIZATIONS_TAB_NAME = 'Concept (Row) Generalizations'
CLEANING_CONFORMANCE_TAB_NAME = 'Cleaning & Conformance'
PROGRAM_CUSTOM_CONCEPT_IDS_TAB_NAME = 'Program Custom Concept IDs'
WEARABLES_TAB_NAME = 'Wearables'

SHEET_NAMES = [
    CHANGE_LOG_TAB_NAME,
    AVAILABLE_FIELDS_TAB_NAME,
    TABLE_SUPPRESSIONS_TAB_NAME,
    FIELD_SUPPRESSIONS_TAB_NAME,
    CONCEPT_SUPPRESSIONS_TAB_NAME,
    FIELD_GENERALIZATIONS_TAB_NAME,
    CONCEPT_GENERALIZATIONS_TAB_NAME,
    CLEANING_CONFORMANCE_TAB_NAME,
    PROGRAM_CUSTOM_CONCEPT_IDS_TAB_NAME,
    WEARABLES_TAB_NAME,
]

# Formats
ALL = 'all'
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
FILENAME_DATE_FORMAT = '%Y%m%d'

# File names
DEFAULT_LOG = 'LOGS/generate_yaml.log'
YAML_OUTPUT_FILENAME = 'yaml_files/CDRDD_{cdr_version}_{today}.yaml'

# Regular expressions
HYPERLINK_REGEX = r'=HYPERLINK\("(?P<link>.+)","(?P<text>.+)"\)'
URL_REGEX = (r'(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?'
             r'[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')

BLANK_VALUE = ['']

INIT_META_DATA_VALUES = {
    'last_modifying_user_display_name': None,
    'name': None,
    'last_modifying_user_email_address': None,
    'modified_time': None,
    'version': None,
    'created_time': None,
    'id': None,
    'cdr_version': None
}

INIT_AVAILABLE_FIELDS_VALUES = {
    'relevant_omop_table': BLANK_VALUE,
    'field_name': BLANK_VALUE,
    'omop_cdm_standard_or_custom_field': BLANK_VALUE,
    'description': BLANK_VALUE,
    'field_type': BLANK_VALUE,
    'data_provenance': BLANK_VALUE,
    'source_ppi_module': BLANK_VALUE,
    'transformed_by_registered_tier_privacy_methods': BLANK_VALUE,
    'transformation_applied_(registered_tier)': BLANK_VALUE,
    'transformed_by_privacy_methodology_(controlled_tier)': BLANK_VALUE,
    'transformation_applied_(controlled_tier)': BLANK_VALUE,
    'data_cleaning_rule_(cdr_clean)': BLANK_VALUE,
    'additional_notes': BLANK_VALUE
}

INIT_CHANGE_LOG_VALUES = {
    'change_number': BLANK_VALUE,
    'change_description': BLANK_VALUE,
    'date_requested': BLANK_VALUE,
    'date_completed': BLANK_VALUE,
    'cdr_version': BLANK_VALUE,
    'completed_by': BLANK_VALUE
}

INIT_ROW_GENERALIZATIONS = {
    'relevant_omop_table': BLANK_VALUE,
    'field_name': BLANK_VALUE,
    'concept_name': BLANK_VALUE,
    'concept_id': BLANK_VALUE,
    'data_provenance': BLANK_VALUE,
    'source_ppi_module': BLANK_VALUE,
    'transformation_applied_in_registered_tier': BLANK_VALUE,
    'registered_tier_transformation_description': BLANK_VALUE,
    'fields_affected': BLANK_VALUE,
    'input_concept_id': BLANK_VALUE,
    'input_concept_name': BLANK_VALUE,
    'generalized_output_concept_id': BLANK_VALUE,
    'generalized_output_concept_name': BLANK_VALUE,
    'transformed_by_privacy_methodology_(controlled_tier)': BLANK_VALUE,
    'transformation_applied_(controlled_tier)': BLANK_VALUE,
    'data_cleaning_rule_(cdr_clean)': BLANK_VALUE,
    'additional_notes': BLANK_VALUE
}

INIT_ROW_SUPPRESSIONS = {
    'relevant_omop_table': BLANK_VALUE,
    'field_name': BLANK_VALUE,
    'concept_name': BLANK_VALUE,
    'concept_id': BLANK_VALUE,
    'data_provenance': BLANK_VALUE,
    'source_ppi_module': BLANK_VALUE,
    'transformation_applied_in_registered_tier': BLANK_VALUE,
    'privacy_output_in_registered_tier': BLANK_VALUE,
    'transformed_by_privacy_methodology_(controlled_tier)': BLANK_VALUE,
    'transformation_applied_(controlled_tier)': BLANK_VALUE,
    'data_cleaning_rule_(cdr_clean)': BLANK_VALUE,
    'additional_notes': BLANK_VALUE
}

INIT_COL_GENERALIZATIONS = {
    'relevant_omop_table': BLANK_VALUE,
    'field_name': BLANK_VALUE,
    'omop_cdm_standard_or_custom_field': BLANK_VALUE,
    'description': BLANK_VALUE,
    'field_type': BLANK_VALUE,
    'data_provenance': BLANK_VALUE,
    'source_ppi_module': BLANK_VALUE,
    'transformed_by_registered_tier_privacy_methods': BLANK_VALUE,
    'transformation_applied_in_registered_tier': BLANK_VALUE,
    'privacy_output_in_registered_tier': BLANK_VALUE,
    'transformed_by_privacy_methodology_(controlled_tier)': BLANK_VALUE,
    'transformation_applied_(controlled_tier)': BLANK_VALUE,
    'data_cleaning_rule_(cdr_clean)': BLANK_VALUE,
    'additional_notes': BLANK_VALUE
}

INIT_COL_SUPPRESSIONS = {
    'relevant_omop_table': BLANK_VALUE,
    'field_name': BLANK_VALUE,
    'omop_cdm_standard_or_custom_field': BLANK_VALUE,
    'description': BLANK_VALUE,
    'field_type': BLANK_VALUE,
    'data_provenance': BLANK_VALUE,
    'source_ppi_module': BLANK_VALUE,
    'transformed_by_registered_tier_privacy_methods': BLANK_VALUE,
    'transformation_applied_in_registered_tier': BLANK_VALUE,
    'privacy_output_in_registered_tier': BLANK_VALUE,
    'transformed_by_privacy_methodology_(controlled_tier)': BLANK_VALUE,
    'transformation_applied_(controlled_tier)': BLANK_VALUE,
    'data_cleaning_rule_(cdr_clean)': BLANK_VALUE,
    'additional_notes': BLANK_VALUE
}


INIT_TABLE_SUPPRESSIONS = {
    'relevant_omop_table': BLANK_VALUE,
    'omop_cdm_standard_or_custom_field': BLANK_VALUE,
    'description': BLANK_VALUE,
    'data_provenance': BLANK_VALUE,
    'transformed_by_registered_tier_privacy_methods': BLANK_VALUE,
    'transformation_applied_in_registered_tier': BLANK_VALUE,
    'privacy_output_in_registered_tier': BLANK_VALUE,
    'transformed_by_privacy_methodology_(controlled_tier)': BLANK_VALUE,
    'transformation_applied_(controlled_tier)': BLANK_VALUE,
    'data_cleaning_rule_(cdr_clean)': BLANK_VALUE,
    'additional_notes': BLANK_VALUE
}

INIT_CLEAN_CONFORM_VALUES = {
    'rule_name': BLANK_VALUE,
    'rule_description': BLANK_VALUE,
    'cdr_impacted': BLANK_VALUE,
    'tables_affected': BLANK_VALUE,
    'fields_affected': BLANK_VALUE,
    'outputs': BLANK_VALUE,
    'notes': BLANK_VALUE
}

INIT_CUSTOM_CONCEPTS = {
    'relevant_omop_table': BLANK_VALUE,
    'concept_id': BLANK_VALUE,
    'concept_name': BLANK_VALUE,
    'concept_code': BLANK_VALUE,
    'description': BLANK_VALUE
}

INIT_WEARABLES = {
    'table': BLANK_VALUE,
    'level': BLANK_VALUE,
    'field': BLANK_VALUE,
    'data_type': BLANK_VALUE,
    'affected_by_privacy_methodology': BLANK_VALUE,
    'transformation': BLANK_VALUE,
}
