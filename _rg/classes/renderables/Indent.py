from dataclasses import dataclass

from _rg.classes.RenderSettings import RenderSettings, RenderMode
from _rg.classes.renderables.Renderable import Renderable


@dataclass
class Indent(Renderable):
    contents: list[str | Renderable]

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        if RenderSettings.render_mode == RenderMode.PDF:
            return [r"\setlength{\parindent}{\parindent+4mm}" + "\n\n" + r"\nopagebreak"] + \
                self.contents + \
                [r"\setlength{\parindent}{\parindent-4mm}"]
        else:
            return self.contents