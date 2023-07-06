from dataclasses import dataclass

from zsil import colors

from _rg.classes.RenderSettings import RenderSettings, RenderMode
from _rg.classes.renderables.WithEmphasis import WithEmphasis
from _rg.classes.renderables.Renderable import Renderable
from _rg.general import tex_escape


@dataclass
class Heading(Renderable):
    text: str
    steps_in: int

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        if render_settings.render_mode == RenderMode.PDF:
            letters = []
            if render_settings.title_gradients:
                for letter_index, letter in enumerate(self.text):
                    text_progress = letter_index / (len(self.text) - 1)
                    current_color = colors.merge_colors(render_settings.start_color_at(self.steps_in),
                                                       render_settings.secondary_color,
                                                       text_progress)
                    no_page_break = "" # r"\nopagebreak " if letter_index <= 0 else ""
                    letters.append(fr"\color[RGB]{{{str(current_color)[1:-1]}}}{{{no_page_break}{{{tex_escape(letter)}}}}}")
            else:
                letters.append(self.text)

            return [
                WithEmphasis(self.steps_in, ["".join(letters)]), # Line breaks cause gaps, so
            ]
        else:
            return ["\n" + self.text.upper()]

    def __str__(self):
        return f"{self.__class__.__name__} whose content is {self.text}"