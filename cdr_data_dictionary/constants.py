SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
]

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

INTEGER_FIELDS = [
    CONCEPT_ID_FIELD,
    GENERALIZED_CONCEPT_ID_FIELD,
    VERSION,
]

BOOLEAN_FIELDS = [
    REGISTERED_TRANSFORM_FIELD,
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

SHEET_NAMES = [
    CHANGE_LOG_TAB_NAME,
    AVAILABLE_FIELDS_TAB_NAME,
    TABLE_SUPPRESSIONS_TAB_NAME,
    FIELD_SUPPRESSIONS_TAB_NAME,
    CONCEPT_SUPPRESSIONS_TAB_NAME,
    FIELD_GENERALIZATIONS_TAB_NAME,
    CONCEPT_GENERALIZATIONS_TAB_NAME,
    CLEANING_CONFORMANCE_TAB_NAME,
]

# Formats
ALL = 'all'
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
FILENAME_DATE_FORMAT = '%Y%m%d'

# File names
DEFAULT_LOG = 'LOGS/generate_yaml.log'
YAML_OUTPUT_FILENAME = '../yaml_files/CDRDD_{cdr_version}_{today}.yaml'

# Regular expressions
HYPERLINK_REGEX = '=HYPERLINK\("(?P<link>.+)","(?P<text>.+)"\)'
URL_REGEX = '(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'

BLANK_VALUE = [u'']

INIT_META_DATA_VALUES = {
    u'last_modifying_user_display_name': None,
    u'name': None,
    u'last_modifying_user_email_address': None,
    u'modified_time': None,
    u'version': None,
    u'created_time': None,
    u'id': None,
    u'cdr_version': None
}

INIT_AVAILABLE_FIELDS_VALUES = {
    u'relevant_omop_table': BLANK_VALUE,
    u'field_name': BLANK_VALUE,
    u'omop_cdm_standard_or_custom_field': BLANK_VALUE,
    u'description': BLANK_VALUE,
    u'field_type': BLANK_VALUE,
    u'data_provenance': BLANK_VALUE,
    u'source_ppi_module': BLANK_VALUE,
    u'transformed_by_registered_tier_privacy_methods': BLANK_VALUE,
    u'transformation_applied_(registered_tier)': BLANK_VALUE,
    u'transformed_by_privacy_methodology_(controlled_tier)': BLANK_VALUE,
    u'transformation_applied_(controlled_tier)': BLANK_VALUE,
    u'data_cleaning_rule_(cdr_clean)': BLANK_VALUE,
    u'additional_notes': BLANK_VALUE
}

INIT_CHANGE_LOG_VALUES = {
    u'change_number': BLANK_VALUE,
    u'change_description': BLANK_VALUE,
    u'date_requested': BLANK_VALUE,
    u'date_completed': BLANK_VALUE,
    u'cdr_version': BLANK_VALUE,
    u'completed_by': BLANK_VALUE
}

INIT_ROW_GENERALIZATIONS = {
    u'relevant_omop_table': BLANK_VALUE,
    u'field_name': BLANK_VALUE,
    u'concept_name': BLANK_VALUE,
    u'concept_id': BLANK_VALUE,
    u'data_provenance': BLANK_VALUE,
    u'source_ppi_module': BLANK_VALUE,
    u'transformation_applied_in_registered_tier': BLANK_VALUE,
    u'registered_tier_transformation_description': BLANK_VALUE,
    u'fields_affected': BLANK_VALUE,
    u'input_concept_id': BLANK_VALUE,
    u'input_concept_name': BLANK_VALUE,
    u'generalized_output_concept_id': BLANK_VALUE,
    u'generalized_output_concept_name': BLANK_VALUE,
    u'transformed_by_privacy_methodology_(controlled_tier)': BLANK_VALUE,
    u'transformation_applied_(controlled_tier)': BLANK_VALUE,
    u'data_cleaning_rule_(cdr_clean)': BLANK_VALUE,
    u'additional_notes': BLANK_VALUE
}

INIT_ROW_SUPPRESSIONS = {
    u'relevant_omop_table': BLANK_VALUE,
    u'field_name': BLANK_VALUE,
    u'concept_name': BLANK_VALUE,
    u'concept_id': BLANK_VALUE,
    u'data_provenance': BLANK_VALUE,
    u'source_ppi_module': BLANK_VALUE,
    u'transformation_applied_in_registered_tier': BLANK_VALUE,
    u'privacy_output_in_registered_tier': BLANK_VALUE,
    u'transformed_by_privacy_methodology_(controlled_tier)': BLANK_VALUE,
    u'transformation_applied_(controlled_tier)': BLANK_VALUE,
    u'data_cleaning_rule_(cdr_clean)': BLANK_VALUE,
    u'additional_notes': BLANK_VALUE
}

INIT_COL_GENERALIZATIONS = {
    u'relevant_omop_table': BLANK_VALUE,
    u'field_name': BLANK_VALUE,
    u'omop_cdm_standard_or_custom_field': BLANK_VALUE,
    u'description': BLANK_VALUE,
    u'field_type': BLANK_VALUE,
    u'data_provenance': BLANK_VALUE,
    u'source_ppi_module': BLANK_VALUE,
    u'transformed_by_registered_tier_privacy_methods': BLANK_VALUE,
    u'transformation_applied_in_registered_tier': BLANK_VALUE,
    u'privacy_output_in_registered_tier': BLANK_VALUE,
    u'transformed_by_privacy_methodology_(controlled_tier)': BLANK_VALUE,
    u'transformation_applied_(controlled_tier)': BLANK_VALUE,
    u'data_cleaning_rule_(cdr_clean)': BLANK_VALUE,
    u'additional_notes': BLANK_VALUE
}

INIT_COL_SUPPRESSIONS = {
    u'relevant_omop_table': BLANK_VALUE,
    u'field_name': BLANK_VALUE,
    u'omop_cdm_standard_or_custom_field': BLANK_VALUE,
    u'description': BLANK_VALUE,
    u'field_type': BLANK_VALUE,
    u'data_provenance': BLANK_VALUE,
    u'source_ppi_module': BLANK_VALUE,
    u'transformed_by_registered_tier_privacy_methods': BLANK_VALUE,
    u'transformation_applied_in_registered_tier': BLANK_VALUE,
    u'privacy_output_in_registered_tier': BLANK_VALUE,
    u'transformed_by_privacy_methodology_(controlled_tier)': BLANK_VALUE,
    u'transformation_applied_(controlled_tier)': BLANK_VALUE,
    u'data_cleaning_rule_(cdr_clean)': BLANK_VALUE,
    u'additional_notes': BLANK_VALUE
}


INIT_TABLE_SUPPRESSIONS = {
    u'relevant_omop_table': BLANK_VALUE,
    u'omop_cdm_standard_or_custom_field': BLANK_VALUE,
    u'description': BLANK_VALUE,
    u'data_provenance': BLANK_VALUE,
    u'transformed_by_registered_tier_privacy_methods': BLANK_VALUE,
    u'transformation_applied_in_registered_tier': BLANK_VALUE,
    u'privacy_output_in_registered_tier': BLANK_VALUE,
    u'transformed_by_privacy_methodology_(controlled_tier)': BLANK_VALUE,
    u'transformation_applied_(controlled_tier)': BLANK_VALUE,
    u'data_cleaning_rule_(cdr_clean)': BLANK_VALUE,
    u'additional_notes': BLANK_VALUE
}

INIT_CLEAN_CONFORM_VALUES = {
    u'rule_name': BLANK_VALUE,
    u'rule_description': BLANK_VALUE,
    u'cdr_impacted': BLANK_VALUE,
    u'tables_affected': BLANK_VALUE,
    u'fields_affected': BLANK_VALUE,
    u'outputs': BLANK_VALUE,
    u'notes': BLANK_VALUE
}
