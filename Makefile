.PHONY: all install-dev test qa

all:

install-dev:
	pip3 install -r requirements/requirements.txt --no-binary :all:
	pip3 install -r requirements/requirements-dev-1.txt --no-binary :all:
	pip3 install -r requirements/requirements-dev-2.txt --no-binary :all:
	pip3 install -r requirements/requirements-dev-3.txt --no-binary :all:

test:
	python3 -m pytest

#coverage run -m pytest -v
#coverage report -m
qa:
	isort --check-only --diff --recursive .
	pycodestyle .
	pyflakes setup.py frami
	pylint --output-format parseable setup.py frami tests
	yapf --diff --recursive .
	safety check --bare --cache
	ossaudit \
		--file requirements/requirements.txt \
		--file requirements/requirements-dev-1.txt \
		--file requirements/requirements-dev-2.txt \
		--file requirements/requirements-dev-3.txt
