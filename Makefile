init:
	chmod -R +x .githooks
	git config core.hooksPath .githooks

install:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

lint:
	command -v flake8 || pip install --upgrade flake8
	flake8

test:
	command -v pytest || pip install --upgrade pytest pytest-cov pytest-subtests pytest-django
	pytest

check:
	python -Wa manage.py check
	python -Wa manage.py check --deploy
	python -Wa manage.py makemigrations --check

collectstatic:
	python -Wa manage.py collectstatic --no-input

makemigrations:
	python -Wa manage.py makemigrations --no-input

migrate:
	python -Wa manage.py migrate --no-input

clean:
	find . -type f -name '*.pyc' -exec rm -rf {} \;
	find . -type f -name '*.pyo' -exec rm -rf {} \;
	find . -type f -name '*.coverage' -exec rm -rf {} \;
	find . -depth -type d -name '__pycache__' -exec rm -rf {} \;
	find . -depth -type d -name '.pytest_cache' -exec rm -rf {} \;
