CODE_FOLDERS := server
TEST_FOLDERS := tests

.PHONY: update test lint security_checks

install:
	poetry install

update:
	poetry lock

test:
	poetry run pytest

format:
	black .

lint:
	black --check .
	flake8 $(CODE_FOLDERS) $(TEST_FOLDERS)
	mypy $(CODE_FOLDERS) $(TEST_FOLDERS)
	pylint $(CODE_FOLDERS) $(TEST_FOLDERS)

security_checks:
	bandit -r $(CODE_FOLDERS)