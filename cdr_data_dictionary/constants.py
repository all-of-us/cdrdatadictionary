SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
INTEGER_FIELDS = ['concept_id', 'generalized_output_concept_id', 'input_concept_id']
BOOLEAN_FIELDS = ['transformed_by_registered_tier_privacy_methods']
DATE_FIELDS = ['date_requested', 'date_completed']
SHEET_NAMES = [
    'Change Log',
    'Available Fields',
    'Table Suppressions',
    'Field (Column) Suppressions',
    'Concept (Row) Suppressions',
    'Field (Column) Generalizations',
    'Concept (Row) Generalizations'
]
ALL = 'all'
DATE_FORMAT = '%Y-%m-%d'

DEFAULT_LOG = 'LOGS/generate_yaml.log'
