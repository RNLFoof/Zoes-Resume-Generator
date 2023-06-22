import pathlib
import re
from dataclasses import dataclass

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.Renderable import Renderable
from _rg.definitions import IMAGE_DIR


@dataclass
class IconLink(Renderable):
    url: str

    def icon_name(self) -> str:
        """Returns the name of the relevant icon, which is the second level domain name of the url.

        Returns
        -------
            The aforementioned icon name.
        """
        match = re.match(r"https?://.*\.(.*?)\.", self.url)
        if match is None:
            match = re.match(r"https?://(.+?)\.", self.url)
        if match is None:
            raise Exception(f'Unable to get a second level domain name from the url "{self.url}", consider not feeding me garbage.')
        return match.group(1)

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [
            r"\makeatletter",
            r"\newcommand*\fsize{\dimexpr\f@size mm\relax}",
            r"\makeatother",
            fr"\graphicspath{{ {{{pathlib.PureWindowsPath(IMAGE_DIR).as_posix()}}} }}",
            fr"\includegraphics[width=\fsize]{{ icons/{self.icon_name()} }}"
        ]
