from dataclasses import dataclass

from zsil import colors

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.ChangeEmphasis import ChangeEmphasis
from _rg.classes.renderables.Renderable import Renderable
from _rg.general import tex_escape


@dataclass
class Heading(Renderable):
    text: str
    steps_in: int

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        letters = []
        if render_settings.title_gradients:
            for letter_index, letter in enumerate(self.text):
                text_progress = letter_index / (len(self.text) - 1)
                current_color = colors.mergecolors(render_settings.start_color_at(self.steps_in),
                                                   render_settings.secondary_color,
                                                   text_progress)
                letters.append(fr"\color[RGB]{{{str(current_color)[1:-1]}}}{{{tex_escape(letter)}}}")
        else:
            letters.append(self.text)

        return [
            ChangeEmphasis(self.steps_in),
            "".join(letters)  # Line breaks cause gaps, so
        ]
