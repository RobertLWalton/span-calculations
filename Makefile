all:	equations.pdf span.pdf weight.pdf

equations equations.pdf:	equations.tex
	rm -f equations.pdf
	pdflatex equations

span.txt:	span.py
	rm -f span.txt
	python3 span.py > span.txt

span.pdf:	span.txt
	rm -f span.pdf
	print -2No span.txt > span.pdf

weight.txt:	weight.py
	rm -f weight.txt
	python3 weight.py > weight.txt

weight.pdf:	weight.txt
	rm -f weight.pdf
	print -2No weight.txt > weight.pdf
