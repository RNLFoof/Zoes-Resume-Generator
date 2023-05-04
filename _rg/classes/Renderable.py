import os
import subprocess
from typing import TypeVar, Self, Any

from zsil import colors

from _rg.classes.RenderSettings import RenderSettings
from _rg.general import tex_change_emphasis

RecursiveStrList = TypeVar("RecursiveStrList", list[str], list[Self])


class Renderable:
    def render(self, render_settings: RenderSettings) -> RecursiveStrList:
        raise NotImplementedError()

    def render_as_string(self, render_settings: RenderSettings) -> str:
        def flatten(l: RecursiveStrList) -> list[str]:
            output = []
            for item in l:
                if type(item) is list:
                    output += ["\t" + x for x in flatten(item)]
                else:
                    output.append(item)
            return output

        return "\n".join(
            flatten(
                self.render(render_settings)
            )
        )

    def generate_tex(self, directory: str, render_settings: RenderSettings):
        from _rg.classes.Heading import Heading
        global_variables = {
            "primary_color": colors.tuple_to_hex(render_settings.primary_color),
            "secondary_color": colors.tuple_to_hex(render_settings.secondary_color),
            "zoe": "".join(Heading("ZOE ZABLOTSKY", 0).render_as_string(render_settings))
        }
        for n in range(10):
            global_variables[f"change_emphasis_to_{n}"] = "".join(tex_change_emphasis(n))

        with open(f"{directory}/{self.__class__.__name__}.tex", "w") as f:
            f.write(self.generate_tex_section("start", global_variables)),
            f.write(self.render_as_string(render_settings))
            f.write(self.generate_tex_section("end", global_variables)),

    def generate_pdf(self, directory: str, render_settings: RenderSettings):
        self.generate_tex(directory, render_settings)
        subprocess.run(["pdflatex", "-output-directory=out", f"{directory}/{self.__class__.__name__}.tex"])

    def generate_tex_section(self, section_name, variables: dict[str, Any]):
        with open(
                os.path.join(
                    os.path.abspath(os.path.split(__file__)[0]),
                    fr"../tex/{section_name}.tex"
                ), "r") as f:
            s = f.read()
        for name, value in variables.items():
            s = s.replace(f"__{name}__", value)
        return s

    @staticmethod
    def tex_table(table: list[list["Renderable"]], render_settings: RenderSettings, horizontal_lines=False,
                  vertical_lines=False) -> RecursiveStrList:
        column_count = max(len(row) for row in table)
        l = []
        l.append(rf"\SetTblrInner{{rowsep=0mm, leftsep=1mm, rightsep=4mm}}")
        if vertical_lines:
            l.append(fr"\begin{{tblr}}{{|{'l|' * column_count}}}")
        else:
            l.append(fr"\begin{{tblr}}{{{'l' * column_count}}}")

        l.append(r"\hline" if horizontal_lines else "")

        for row in table:
            if len(row) == column_count:
                l.append(" & ".join([
                    cell.render_as_string(render_settings)
                    if issubclass(cell.__class__, Renderable)
                    else str(cell)
                    for cell in row
                ]))
            elif len(row) == 1:
                l.append(fr"\SetCell[c={column_count}]{{l}}" + row[0].render_as_string(render_settings))
            else:
                raise NotImplementedError()
            l.append(r"\\" + (r"\hline" if horizontal_lines else "") + "\n")

        l.append(r"\end{tblr}")
        return l
