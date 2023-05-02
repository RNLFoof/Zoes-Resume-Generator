from dataclasses import dataclass
from enum import Enum

from zsil import colors


class color(Enum):
    AZURE = (55, 95, 173)
    DARK_BLUE = (4, 5, 132)
    PASTEL_PURPLE = (212, 198, 216)
    DEEP_PURPLE = (44, 17, 79)

@dataclass
class RenderSettings:
    title_gradients = True

    largest_text_size = 24

    primary_color = color.AZURE.value
    secondary_color = colors.mergecolors(color.DEEP_PURPLE.value, color.PASTEL_PURPLE.value, 0.5)
    link_color = color.AZURE.value
    first_black_step = 3

    def start_color_at(self, steps_in: int):
        return colors.mergecolors(self.primary_color, self.secondary_color,
                                  steps_in / (self.first_black_step - 1))
