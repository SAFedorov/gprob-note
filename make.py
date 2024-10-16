import os
import re


texdir = "tex-pdf"

os.chdir(texdir) 

texcmd = "pdflatex -interaction=nonstopmode note.tex"
if not os.path.isfile("note.aux"):
    os.system(texcmd)      # Compiles without the bibliography first.

os.system(f"bibtex note")  # Compiles the bibliography.
os.system(texcmd)          # Recompiles with the bibliography.

os.chdir(os.pardir)


# Inserts the bibliography directly in the compiled tex file.
with open(os.path.join(texdir, "note.tex"), "r", encoding="utf-8") as file:
    contents = file.read()

with open(os.path.join(texdir, "note.bbl"), "r", encoding="utf-8") as file:
    bbl = file.read()

contents = contents.replace(r"\bibliography{references}", bbl)

with open("note_.tex", "w", encoding="utf-8") as file:
    file.write(contents)


# Converts to html.
os.system("latexml --destination note.xml note_.tex")
os.system("latexmlpost --css my.css --javascript=LaTeXML-maybeMathjax.js "
          "--destination index.html note.xml")


with open("index.html", "r", encoding="utf-8") as file:
    contents = file.read()

contents = re.sub(r"\[Online\]\.\s+Available:\s*", "", contents)
contents = re.sub(r"<footer.*</footer>", "", contents, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as file:
    file.write(contents)