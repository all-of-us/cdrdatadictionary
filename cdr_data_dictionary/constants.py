SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
]

INTEGER_FIELDS = [
    'concept_id',
    'generalized_output_concept_id',
    'input_concept_id',
    'version',
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
]

ALL = 'all'
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DEFAULT_LOG = 'LOGS/generate_yaml.log'
