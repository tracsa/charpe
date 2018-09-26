.PHONY: release clean test lint

release:
	./setup.py test && ./setup.py sdist && ./setup.py bdist_wheel && twine upload dist/* && git push && git push --tags

clean:
	rm -rf dist/

test: pytest lint

pytest:
	pytest -xvv

lint:
	flake8 --exclude=.env,.tox,dist,docs,build,*.egg .
