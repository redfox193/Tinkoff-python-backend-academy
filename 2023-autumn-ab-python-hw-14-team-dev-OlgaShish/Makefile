CODE_FOLDERS := src
TEST_FOLDERS := tests

.PHONY: update test lint

install:
	poetry install --no-root

update:
	poetry lock
	poetry install --no-root

test:
	pytest $(TEST_FOLDER) --cov=$(CODE_FOLDERS)

format:
	poetry run black .

lint:
	poetry run black --check .
	poetry run flake8 $(CODE_FOLDERS) $(TEST_FOLDERS)