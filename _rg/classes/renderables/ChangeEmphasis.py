from dataclasses import dataclass

from zsil import colors

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.Renderable import Renderable


@dataclass
class ChangeEmphasis(Renderable):
    steps_in: int

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        if render_settings is None:
            render_settings = RenderSettings()
        black = (0, 0, 0)
        first_black_step = 3
        if self.steps_in >= first_black_step:
            current_color = black
        else:
            # current_color = tuple([int(band * pow(0.5, steps_in)) for band in highlight_color])
            current_color = colors.mergecolors(render_settings.primary_color, render_settings.secondary_color,
                                               self.steps_in / (first_black_step - 1))
            # current_color = tuple(
            #     [int(band / first_black_step * (first_black_step - steps_in)) for band in highlight_color])
        final_color_string = colors.tuple_to_hex(current_color)
        return [
            fr"\fontsize{{{render_settings.text_curve_at(self.steps_in) * 0.75}mm}}"
            fr"{{{render_settings.text_curve_at(self.steps_in)}mm}}\selectfont",
            fr"\color[RGB]{{{str(current_color)[1:-1]}}}"
        ]
