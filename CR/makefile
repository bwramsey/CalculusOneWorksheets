PROJECT=chainRule
TEX=pdflatex
BUILDHTEX=pdflatex --jobname=$(PROJECT) '\newcommand\HCCondition{0}\input{$(PROJECT).tex}'
BUILDSTEX=pdflatex --jobname=$(PROJECT)Soln '\newcommand\HCCondition{1}\input{$(PROJECT).tex}'

all: handout soln clean

handout:
	$(BUILDHTEX)
	$(BUILDHTEX)

soln:
	$(BUILDSTEX)
	$(BUILDSTEX)

clean-all:
	rm -f *.dvi *.log *.bak *.aux *.bbl *.blg *.idx *.ps *.eps *.pdf *.toc *.out *~ *.ids *.jax *.oc *.gz

clean:
	rm -f *.log *.bak *.aux *.bbl *.blg *.idx *.toc *.out *~ *.ids *.jax *.oc *.gz
