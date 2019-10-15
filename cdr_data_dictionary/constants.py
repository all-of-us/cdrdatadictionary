SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
]

INTEGER_FIELDS = [
    'concept_id',
    'generalized_output_concept_id',
    'version',
]

MULTIPLE_TYPES = [
    'input_concept_id',
]

BOOLEAN_FIELDS = [
    'transformed_by_registered_tier_privacy_methods',
]

TEMPORAL_FIELDS = [
    'date_requested',
    'date_completed',
    'created_time',
    'modified_time',
]

SHEET_NAMES = [
    'Change Log',
    'Available Fields',
    'Table Suppressions',
    'Field (Column) Suppressions',
    'Concept (Row) Suppressions',
    'Field (Column) Generalizations',
    'Concept (Row) Generalizations',
    'Cleaning & Conformance',
]

ALL = 'all'
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DEFAULT_LOG = 'LOGS/generate_yaml.log'

HYPERLINK_REGEX = '=HYPERLINK\("(?P<link>.+)","(?P<text>.+)"\)'

URL_REGEX = '(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'

BLANK_VALUE = [u'']

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
