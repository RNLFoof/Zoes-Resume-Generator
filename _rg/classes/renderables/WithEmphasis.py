from dataclasses import dataclass
from zsil import colors

from _rg.classes.RenderSettings import RenderSettings, RenderFormat
from _rg.classes.renderables.Renderable import Renderable


@dataclass
class WithEmphasis(Renderable):
    steps_in: int
    content: list[str | Renderable]
    no_break: bool = False

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        if render_settings.render_format != RenderFormat.LATEX:
            return self.content

        if render_settings is None:
            render_settings = RenderSettings()
        black = (0, 0, 0)
        first_black_step = 3
        if self.steps_in >= first_black_step:
            current_color = black
        else:
            # current_color = tuple([int(band * pow(0.5, steps_in)) for band in highlight_color])
            current_color = colors.merge_colors(render_settings.primary_color, render_settings.secondary_color,
                                               self.steps_in / (first_black_step - 1))
            # current_color = tuple(
            #     [int(band / first_black_step * (first_black_step - steps_in)) for band in highlight_color])
        final_color_string = colors.tuple_to_hex(current_color)
        total_size = render_settings.text_curve_at(self.steps_in)
        font_size = total_size * render_settings.margin_to_text_ratio
        baseline_skip = total_size
        return [
            fr"{{\color[RGB]{{{str(current_color)[1:-1]}}}""\n"fr"\fontsize{{{font_size}mm}}{{{baseline_skip}mm}}\selectfont" #+
            #("" if self.no_break else r"\par""\n")
            ] + self.content + [
            r"\par}"
        ]
