from dataclasses import dataclass
from enum import Enum

from zsil import colors


class color(Enum):
    AZURE = (55, 95, 173)
    DARK_BLUE = (4, 5, 132)
    PASTEL_PURPLE = (212, 198, 216)
    DEEP_PURPLE = (44, 17, 79)
    FUCHSIA = (254, 65, 100)
    CELESTE_CYAN = (58, 189, 225)
    CELESTE_BLUE = (58, 105, 225)
    CELESTE_PURPLE = (108, 29, 169)

class curve(Enum):
    HALVING = lambda self, x: 0.5 ** x
    THREE_QUARTERING = lambda self, x: 0.75 ** x


@dataclass
class RenderSettings:
    title_gradients = True

    margin_to_text_ratio = 0.75

    largest_text_size = 24
    first_text_step = 3
    heading_curve = curve.HALVING
    text_curve = lambda self, x: 0.5 ** x

    primary_color = color.CELESTE_CYAN.value
    secondary_color = color.CELESTE_PURPLE.value
    link_color = color.AZURE.value

    skill_elaboration = False
    show_categories = False
    skill_columns = 4

    def start_color_at(self, steps_in: int):
        return colors.merge_colors(self.primary_color, self.secondary_color,
                                  1 - 0.6 ** steps_in)

    def text_curve_at(self, steps_in: int):
        if steps_in < self.first_text_step:
            return self.largest_text_size * self.heading_curve(steps_in)
        else:
            recentered_steps_in = steps_in - self.first_text_step + 1
            return self.text_curve_at(self.first_text_step - 1) * self.text_curve(recentered_steps_in)
