import re
from typing import Any

from pylatex import Document, Section, Package, Command
from pdflatex import PDFLaTeX
import os
from functools import cache
import subprocess

from _rg.classes.SkillSet import SkillSet


class Resume:
    @cache
    def tex(self):
        skill_set = SkillSet.all()
        skills = skill_set.skills_by_generic_value()

        global_variables = {
            "skills": "\n\n".join([skill.name for skill in skills])
        }

        s = ""
        with open("tex/override.tex", "r") as f:
            override = f.read()
            if override:
                return override
        for section_name in [
            "start",
            "header",
            "skills",
            "end",
        ]:
            s += self.generate_tex_section(section_name, global_variables)
        return s
    
    def generate_tex_section(self, section_name, variables: dict[str, Any]):
        with open(fr"tex/{section_name}.tex", "r") as f:
            s = f.read() + "\n"
        for name, value in variables.items():
            s = s.replace(f"__{name}__", self.tex_escape(value))
        return s

    def generate_tex(self):
        with open("out/resume.tex", "w") as f:
            f.write(self.tex())

    def generate_pdf(self):
        self.generate_tex()
        subprocess.run(["pdflatex", "-output-directory=out", "out/resume.tex"])

    @staticmethod
    def tex_escape(text: str) -> str:
        text = text.replace("\\", r"\textbackslash")
        text = re.sub(r"([&%$#_{}])", r"\\\1", text)
        text = text.replace("~", r"\textasciitilde")
        text = text.replace("^", r"\textasciicircum")
        return text