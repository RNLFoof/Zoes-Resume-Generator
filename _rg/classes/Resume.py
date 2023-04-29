import subprocess
from functools import cache
from typing import Any

from _rg.classes.History import History
from _rg.classes.SkillSet import SkillSet
from _rg.general import tex_change_emphasis


class Resume:
    @cache
    def tex(self):

        global_variables = {
            "skills": SkillSet.summon().tex(),
            "history": History.summon().tex(),
        }

        for n in range(10):
            global_variables[f"change_emphasis_to_{n}"] = tex_change_emphasis(n)

        s = ""
        with open("tex/override.tex", "r") as f:
            override = f.read()
            if override:
                return override
        for section_name in [
            "start",
            "header",
            "skills",
            "history",
            "end",
        ]:
            s += self.generate_tex_section(section_name, global_variables)
        return s
    
    def generate_tex_section(self, section_name, variables: dict[str, Any]):
        with open(fr"tex/{section_name}.tex", "r") as f:
            s = f.read() + "\n"
        for name, value in variables.items():
            s = s.replace(f"__{name}__", value)
        return s

    def generate_tex(self):
        with open("out/resume.tex", "w") as f:
            f.write(self.tex())

    def generate_pdf(self):
        self.generate_tex()
        subprocess.run(["pdflatex", "-output-directory=out", "out/resume.tex"])
