.PHONY: coverage test prereq

apps = blog
manage = manage.py
python = python

prereq:
	echo reminder - must source ../bin/activate

test: prereq
	$(python) $(manage) test $(apps)

coverage: prereq
	coverage run --source='.' $(manage) test $(apps)
	coverage report

