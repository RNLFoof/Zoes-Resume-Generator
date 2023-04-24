from pylatex import Document, Section, Package, Command
from pdflatex import PDFLaTeX
import os
from functools import cache
import subprocess

class Resume:
    @cache
    def tex(self):
        s = ""
        with open("tex/override.tex", "r") as f:
            override = f.read()
            if override:
                return override
        for filename in [
            "tex/start.tex",
            "tex/header.tex",
            "tex/skills.tex",
            "tex/end.tex",
        ]:
            with open(filename, "r") as f:
                s += f.read() + "\n"
        return s

    def generate_tex(self):
        with open("out/resume.tex", "w") as f:
            f.write(self.tex())

    def generate_pdf(self):
        self.generate_tex()
        subprocess.run(["pdflatex", "-output-directory=out", "out/resume.tex"])
