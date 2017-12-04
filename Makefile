.DEFAULT_TARGET := help

MAIN=main

help:
	@echo "make help"
	@echo "    main: compile main.pdf"
	@echo
	@echo "    *Note*: uses \`latexmk' for compilation management. Please install latexmk"
	@echo "            if you do not have it already."


$(MAIN):
	latexmk -pdf $@

clean:
	latexmk -quiet -C $(MAIN)

