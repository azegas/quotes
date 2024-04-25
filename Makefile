######################################### WHAT IS MAKEFILE ##################################################

# we use it in the terminal to run some checks for us manually during the development.

## install make on windows to C:\Program Files (x86)\GnuWin32\bin
## add the path above to user environment variables PATH
## write make in terminal to check if it's reachable/usable
## make sure this file is written with tabs, not spaces. Can use "convert indentation to tabs" in vscode

## In a Makefile, .PHONY is a special target that specifies a list of "phony" targets, which are targets that
# do not correspond to actual files. Instead, they are used to group and organize other targets, or to specify
# commands that should always be executed regardless of whether a file with the same name exists.
# When you declare a target as .PHONY, it tells Make that the target is not a file, so Make will always execute
# the associated commands, even if a file with the same name exists in the directory.


######################################### LINTING ##################################################

# Linting tool performs static code analysis. It checks for code errors,
# code with potentially unintended results and dangerous code patterns.

# some rules that we want to ignore, we put them in .pylintrc file

# have an extension pylint installed in VsCode to do the linting automatically, but this is for "just in case", to see those 10.00/10 ;)

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


######################################### FORMATTING ###############################################

## Formatting tool automatically reformats entire files to a single style.
## It makes code reviews faster and improves collaboration.

# have an extension "Black Formatter" installed in VsCode to do the formatting automatically on save but this is for "just in case", to see those 10.00/10 ;)

.PHONY: black
black:
	python -m black --version
	python -m black .


######################################### TESTING ##################################################

# This target runs Django's test suite. It finds tests in any file named with the pattern test*.py under the current directory and its subdirectories.

.PHONY: test coverage
test:
	python manage.py test

# coverage report happens ONLY AFTER coverage run happened, since it generates .coverage file needed for the report
coverage:
	coverage run manage.py test & coverage report > coverage.txt

######################################### DJANGO STUFF ##################################################

# This target runs Django's test suite. It finds tests in any file named with the pattern test*.py under the current directory and its subdirectories.

.PHONY: mm m run freeze super pre pre-all
m:
	python manage.py migrate & python manage.py migrate --database=postgresql-remote & python manage.py migrate --database=postgresql-local & python manage.py migrate --database=mysql-local

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
