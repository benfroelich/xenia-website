.PHONY: coverage test prereq

manage = manage.py
python = python

prereq:
	$(info reminder - must source ../bin/activate)

test: prereq
	$(python) $(manage) test $(apps)

coverage: prereq
	coverage run --source='.' $(manage) test $(apps)
	coverage report

