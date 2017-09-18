PROJECT='main'

all: bib latex
	pdflatex $(PROJECT)

bib: latex
	bibtex8 $(PROJECT)

latex: 
	latex $(PROJECT)

clean:
	rm *.log *.aux *.out *.bbl *.dvi *.pdf *.blg *.xml *-blx.bib
