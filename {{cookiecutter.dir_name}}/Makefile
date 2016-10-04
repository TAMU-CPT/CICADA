.PHONY: build

install:
	npm install

build:
	./node_modules/.bin/webpack  --progress --colors --devtool source-map

run:
	@echo "**************************************************"
	@echo "* open http://localhost:10000/webpack-dev-server/ *"
	@echo "**************************************************"
	./node_modules/.bin/webpack-dev-server --progress --colors --devtool cheap-module-inline-source-map --hot --debug --inline --host 0.0.0.0 --port 10000
