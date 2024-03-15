CODE_FOLDERS := server
TEST_FOLDERS := tests

.PHONY: update test lint security_checks

install:
	poetry install --no-root

update:
	poetry lock
	poetry install --no-root

test:
	pytest $(TEST_FOLDER) --cov=server

format:
	black .

lint:
	black --check .
	flake8 $(CODE_FOLDERS) $(TEST_FOLDERS)
	pylint $(CODE_FOLDERS) $(TEST_FOLDERS)
	mypy $(CODE_FOLDERS) $(TEST_FOLDERS)