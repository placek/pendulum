TEX=pdflatex
INPUT=report_pl

all: compile

compile:
	$(TEX) $(INPUT).tex

remove_pdf:
	rm -f $(INPUT).pdf

remove_other:
	rm -f $(INPUT).aux
	rm -f $(INPUT).out
	rm -f $(INPUT).log

clean: remove_other remove_pdf
