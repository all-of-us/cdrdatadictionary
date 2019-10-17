#python -m unittest discover -s tests/unit/cdr_data_dictionary/
coverage run -m unittest discover -s tests/unit/cdr_data_dictionary/ -v

coverage report --skip-covered --show-missing
