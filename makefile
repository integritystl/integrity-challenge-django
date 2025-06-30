.PHONY: install format check all

install:
	python3 -m pip install -r requirements.txt

format:
	python3 -m black blog_project

check: install
	python3 -m black blog_project --check
	cd blog_project && python3 manage.py check

# Run format then check
all: format check
