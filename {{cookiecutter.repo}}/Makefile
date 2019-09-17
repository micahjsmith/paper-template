.DEFAULT_GOAL := help
SHELL := /bin/sh

SRCDIR := $(strip $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST)))))
BUILDDIR := $(SRCDIR)/build

export LOCALPAPERBUILD = 1

help:
	@echo "make help"
	@echo "    main: compile main.pdf"
	@echo "    poster: compile poster.pdf"
	@echo "    arxiv: prepare arXiv submission file"
	@echo "    clean: clean LaTeX build files"
	@echo
	@echo "    *Note*: uses \`latexmk' for compilation management. Please install latexmk"
	@echo "            if you do not have it already."


.PHONY: main poster
main: main.pdf
poster: logo poster.pdf

.PHONY: FORCE_MAKE
%.pdf: %.tex _dirs FORCE_MAKE
	latexmk $<

.PHONY: arxiv
arxiv: main
	-rm -rf arxiv
	mkdir arxiv
	pip install -r requirements.txt
	./arxiv.py
	$(MAKE) -C arxiv main
	tar -c -z -f submission.tar.gz -C arxiv . && mv submission.tar.gz arxiv

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)

.PHONY: logo
logo: images/logos/MIT-logo-red-gray.eps _dirs

.PHONY: _dirs
_dirs:
	-@mkdir -p images/logos
	-@mkdir -p $(BUILDDIR)

images/logos/MIT-logo-red-gray.eps:
	$(MAKE) _dirs
	@echo "Use your browser to download the zip file into ./images/logos (MIT certificate required):"
	@echo "   -> https://web.mit.edu/graphicidentity/download/logo-sets/MIT-logos-print.zip"
	@read -p "Press any character to continue when you are done..." -n 1 -s && printf '\n'
	@test -f images/logos/MIT-logos-print.zip || { echo "You failed to download the zip file" && exit 1; }
	unzip -q images/logos/MIT-logos-print.zip -d images/logos && mv images/logos/MIT-logos-print/*.eps images/logos/
	-rm -r images/logos/MIT-logos-print
	-rm -r images/logos/__MACOSX
	-rm images/logos/MIT-logos-print.zip

.PHONY: examples
examples: main poster
	test -d examples || mkdir examples
	cp $(BUILDDIR)/{main,poster}.pdf examples
