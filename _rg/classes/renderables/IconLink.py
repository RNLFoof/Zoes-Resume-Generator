import os.path
import pathlib
import re
from dataclasses import dataclass

from PIL import Image
from zsil.cool_stuff import transfer_alpha

from _rg import definitions
from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.Renderable import Renderable


@dataclass
class IconLink(Renderable):
    url: str

    def original_icon_path(self) -> str:
        return os.path.join(os.path.join(definitions.IMAGE_DIR, "original_icons", self.icon_name() + ".png"))
    def generated_icon_path(self) -> str:
        return os.path.join(os.path.join(definitions.IMAGE_DIR, "generated_icons", self.icon_name() + ".png"))

    def generate_icon(self, render_settings: RenderSettings) -> Image.Image:
        alpha_image = Image.open(self.original_icon_path()).convert("RGBA")
        color_image = Image.new("RGBA", alpha_image.size, render_settings.link_color)
        generated_image = transfer_alpha(alpha_image, color_image)
        generated_image.save(self.generated_icon_path())
        return generated_image

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
            raise Exception(
                f'Unable to get a second level domain name from the url "{self.url}", consider not feeding me garbage.')
        return match.group(1)

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        self.generate_icon(render_settings)

        return [
            fr"\href{{{self.url}}}{{\includegraphics[width=\fsize]{{ {pathlib.PureWindowsPath(self.generated_icon_path()).as_posix()} }}}}"
        ]
