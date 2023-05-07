from dataclasses import dataclass
from enum import Enum

from zsil import colors


class color(Enum):
    AZURE = (55, 95, 173)
    DARK_BLUE = (4, 5, 132)
    PASTEL_PURPLE = (212, 198, 216)
    DEEP_PURPLE = (44, 17, 79)
    FUCHSIA = (254, 65, 100)

class curve(Enum):
    HALVING = lambda self, x: 0.5 ** x
    THREE_QUARTERING = lambda self, x: 0.75 ** x


@dataclass
class RenderSettings:
    title_gradients = True

    largest_text_size = 24
    first_text_step = 3
    Heading_curve = curve.HALVING
    text_curve = lambda self, x: 0.6 ** x

    primary_color = color.AZURE.value
    secondary_color = colors.mergecolors(color.DEEP_PURPLE.value, color.PASTEL_PURPLE.value, 0.5)
    link_color = color.AZURE.value

    def start_color_at(self, steps_in: int):
        return colors.mergecolors(self.primary_color, self.secondary_color,
                                  steps_in / (self.first_text_step - 1))

    def text_curve_at(self, steps_in: int):
        if steps_in < self.first_text_step:
            return self.largest_text_size * self.Heading_curve(steps_in)
        else:
            recentered_steps_in = steps_in - self.first_text_step + 1
            return self.text_curve_at(self.first_text_step - 1) * self.text_curve(recentered_steps_in)
