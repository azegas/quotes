######################################### LINTING ##################################################

.PHONY: lint lint-apps lint-project lint-tests lint-ag_mixins

lint: lint-project lint-apps lint-tests lint-ag_mixins

lint-project:
	python -m pylint --version
	python -m pylint project --rcfile=.pylintrc

lint-apps:
	python -m pylint --version
	python -m pylint apps --rcfile=.pylintrc

lint-tests:
	python -m pylint --version
	python -m pylint tests --rcfile=.pylintrc

lint-ag_mixins:
	python -m pylint --version
	python -m pylint ag_mixins --rcfile=.pylintrc

######################################### FORMATTING ##################################################

.PHONY: black
black:
	python -m black --version
	python -m black .

######################################### TESTS ##################################################

.PHONY: test coverage
test:
	python manage.py test

# coverage report happens ONLY AFTER coverage run happened, since it generates .coverage file needed for the report
coverage:
	coverage run manage.py test & coverage report > coverage.txt

######################################### DJANGO STUFF ##################################################

.PHONY: mm m run freeze super pre pre-all

# m:
# 	python manage.py migrate & python manage.py migrate --database=postgresql-remote & python manage.py migrate --database=postgresql-local & python manage.py migrate --database=mysql-local

m:
	python manage.py migrate

mm:
	python manage.py makemigrations

run:
	python manage.py runserver

freeze:
	pip freeze > requirements.txt

super:
	python manage.py createsuperuser

pre:
	pre-commit run

pre-all:
	pre-commit run --all-files
