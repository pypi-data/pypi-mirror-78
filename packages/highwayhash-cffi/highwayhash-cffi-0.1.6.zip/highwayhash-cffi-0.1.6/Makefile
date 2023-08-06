.PHONY : format readme lint clean build test benchmark wheel source github testpypi pypi

format: readme lint
local: test source wheel
remote: testpypi pypi github
all: local benchmark remote


readme:
	pandoc -f markdown -t rst README.md > README.rst

lint:
	black -l 120 .

clean:
	python setup.py clean --all
	rm -rf .pytest_cache
	rm -rf *.egg-info
	rm -rf .publish
	rm -rf Release

build:
	python build.py
	rm -rf highwayhash/_*.c
	make clean

test: build
	python -m pytest tests/
	make clean

benchmark: build
	python benchmark.py

wheel: format test
	make clean
	python setup.py bdist_wheel --dist-dir=.dist
	make clean

source: format
	tox
	make clean

github-inner:
	mv .gitignore-github .gitignore

	git init
	git config --local user.email "inbox@philonas.net"
	git config --local user.name "Phil Demetriou"

	git add .
	git commit -m "Initial commit"
	git remote add origin https://github.com/kpdemetriou/highwayhash-cffi.git
	git push -f origin master

github: format test clean
	mkdir .publish

	cp -r highwayhash .publish
	cp -r sources .publish
	cp -r tests .publish
	cp .gitignore-github .publish
	cp build.py .publish
	cp LICENSE .publish
	cp MANIFEST.in .publish
	cp README.md .publish
	cp README.rst .publish
	cp setup.py .publish
	cp tox.ini .publish

	make -C .publish -f ../Makefile github-inner
	make clean

testpypi: format test source
	twine upload .dist/$$(ls -t .dist | grep ".zip" | head -n1) -r testpypi

pypi: format test source
	twine upload .dist/$$(ls -t .dist | grep ".zip" | head -n1) -r pypi
