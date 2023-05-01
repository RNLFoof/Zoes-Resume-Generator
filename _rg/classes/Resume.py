import subprocess
from functools import cache
from typing import Any

from zsil import colors

from _rg.classes.Accomplishment import AccomplishmentSet
from _rg.classes.History import History
from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.SkillSet import SkillSet
from _rg.general import tex_change_emphasis, tex_header


class Resume:
    @cache
    def tex(self):
        render_settings = RenderSettings()
        global_variables = {
            "skills": SkillSet.summon().render(),
            "history": History.summon().tex(),
            "accomplishments": AccomplishmentSet.summon().tex(),
            "primary_color": colors.tuple_to_hex(render_settings.primary_color),
            "secondary_color": colors.tuple_to_hex(render_settings.secondary_color),
            "zoe": tex_header("ZOE ZABLOTSKY", 0)
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
            "accomplishments",
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
