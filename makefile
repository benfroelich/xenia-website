.PHONY: coverage test prereq deploycheck

manage = manage.py
python = python

prereq:
	$(info reminder - must source ../bin/activate)

test: prereq
	$(python) $(manage) test $(apps)

coverage: prereq
	coverage run --source='.' $(manage) test $(apps)
	coverage report

deploycheck: prereq
	source prod.sh && $(python) $(manage) check --deploy
