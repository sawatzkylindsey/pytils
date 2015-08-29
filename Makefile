default: build

test:
	coverage run --append --source=pytils -m unittest pytils.tests.all

clean:
	rm -rf build
	rm -rf dist
	rm -rf pytils.egg-info
	coverage erase

build:
	python setup.py sdist

install:
	python setup.py install
