flake8:
	flake8 --doctest papersurfer/*.py

pylint:
	pylint papersurfer/*.py

pycodestyle:
	pycodestyle papersurfer/*

pydocstyle:
	pydocstyle papersurfer/*

pip-prepare:
	- rm -r dist
	python setup.py sdist bdist_wheel
	tar tzf dist/papersurfer*.tar.gz
	twine check dist/*
	
pip-test: pip-prepare
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pip: pip-prepare
	twine upload dist/*
	
lint: flake8 pylint pycodestyle pydocstyle

test:
	python -m pytest --doctest-modules

coverage:
	python -m pytest --doctest-modules --cov=papersurfer
