PY?=python3
BASEDIR=$(CURDIR)
OUTPUTDIR=$(BASEDIR)/output
PORT?=8000

help:
	@echo 'Makefile for Maciej'\''s Dev Blog                                         '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make build                          build the site                     '
	@echo '   make serve                          serve site at http://localhost:8000'
	@echo '   make clean                          remove generated files             '
	@echo '   make dev                            build and serve together           '
	@echo '                                                                          '

build:
	$(PY) build.py

clean:
	[ ! -d "$(OUTPUTDIR)" ] || rm -rf "$(OUTPUTDIR)"

serve: build
	@echo "Serving site at http://localhost:$(PORT)"
	cd "$(OUTPUTDIR)" && $(PY) -m http.server $(PORT)

dev: build serve

.PHONY: build clean serve dev help 