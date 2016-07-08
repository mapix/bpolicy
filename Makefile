test:
	python -m unittest discover tests

test3:
	python3.5 -m unittest discover tests

upload:
	python setup.py sdist upload

