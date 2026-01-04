PROJECT=antiderivatives
TEX=pdflatex
BUILDHTEX=pdflatex --jobname=$(PROJECT) '\newcommand\HCCondition{0}\input{$(PROJECT).tex}'
BUILDSTEX=pdflatex --jobname=$(PROJECT)Soln '\newcommand\HCCondition{1}\input{$(PROJECT).tex}'

ifeq ($(OS),Windows_NT)
    SHELL := powershell.exe
else
   SHELL := powershell
endif
.SHELLFLAGS := -NoProfile -Command 

all: handout soln cleanComma

handout:
	$(BUILDHTEX)
	$(BUILDHTEX)

soln:
	$(BUILDSTEX)
	$(BUILDSTEX)

clean-all:
	rm -f *.dvi *.log *.bak *.aux *.bbl *.sage *.blg *.idx *.ps *.eps *.pdf *.toc *.out *~ *.ids *.jax *.oc *.gz

clean:
	rm -f *.log *.bak *.aux *.bbl *.blg *.sage *.idx *.toc *.out *~ *.ids *.jax *.oc *.gz

cleanComma:
	rm *.log, *.bak, *.aux, *.bbl, *.blg, *.idx, *.toc, *.out, *~, *.ids, *.jax, *.oc, *.gz, *.sage