import os
import pathlib
import re
import subprocess
from typing import Self, Any

import typeguard as typeguard
from zsil import colors

from _rg import definitions
from _rg.classes.RenderSettings import RenderSettings, RenderMode
from _rg.definitions import IMAGE_DIR
from _rg.general import temp_cd


class Renderable:
    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Self]:
        raise NotImplementedError()

    def render_wrapper(self, render_settings: RenderSettings) -> str:
        output = self.class_specific_render(render_settings)
        typeguard.check_type(output, list[str | Renderable])
        for n, x in enumerate(output):
            if issubclass(type(x), Renderable):
                output[n] = x.render_wrapper(render_settings)
            typeguard.check_type(output[n], str)

        output = "\n".join(output)
        output = re.sub(r"^", "\t", output, flags=re.MULTILINE)
        render_description = f"render of {str(self)[:100]}"
        typeguard.check_type(output, str)
        if render_settings.render_mode == RenderMode.PDF:
            return f"%begin {render_description}\n{output}\n%end {render_description}"
        else:
            return output

    def generate_tex(self, directory: str, render_settings: RenderSettings):
        global_variables = {
            "primary_color": colors.tuple_to_hex(render_settings.primary_color),
            "secondary_color": colors.tuple_to_hex(render_settings.secondary_color),
            "graphics_path": pathlib.PureWindowsPath(IMAGE_DIR).as_posix()
        }

        with open(f"{directory}/{self.__class__.__name__}.tex", "w", encoding="UTF8") as f:
            f.write(self.generate_tex_section("start", global_variables))
            f.write("\n")
            f.write(self.render_wrapper(render_settings))
            f.write("\n")
            f.write(self.generate_tex_section("end", global_variables))

    def generate_pdf(self, directory: str, render_settings: RenderSettings):
        self.generate_tex(directory, render_settings)
        with temp_cd(
                directory):  # "...TeX binaries don't allow writing files specified with absolute paths or above the working directory..." https://tex.stackexchange.com/a/328565
            subprocess.run(["pdflatex", f"{self.__class__.__name__}.tex"])

    def generate_tex_section(self, section_name, variables: dict[str, Any]):
        with open(
                os.path.join(
                    definitions.ROOT_DIR,
                    fr"tex/{section_name}.tex"
                ), "r") as f:
            s = f.read()
        for name, value in variables.items():
            s = s.replace(f"__{name}__", value)
        return s

    def generate_txt(self, directory: str, render_settings: RenderSettings):
        with open(f"{directory}/{self.__class__.__name__}.txt", "w", encoding="UTF8") as f:
            f.write(self.render_wrapper(render_settings))

    def __str__(self):
        return self.__class__.__name__

    def generate_file(self, directory: str, render_settings: RenderSettings):
        if render_settings.render_mode == RenderMode.PDF:
            self.generate_pdf(directory, render_settings)
        else:
            self.generate_txt(directory, render_settings)