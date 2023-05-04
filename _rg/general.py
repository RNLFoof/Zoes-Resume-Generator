import importlib
import os
import re
from contextlib import contextmanager

from zsil import colors

from _rg.classes.RenderSettings import RenderSettings


def tex_escape(text: str) -> str:
    text = text.replace("\\", r"\textbackslash")
    text = re.sub(r"([&%$#_{}])", r"\\\1", text)
    text = text.replace("~", r"\textasciitilde")
    text = text.replace("^", r"\textasciicircum")
    return text


def tex_change_emphasis(steps_in: int, render_settings: RenderSettings = None):
    # TODO There's absolutely a way to do this within the bounds of latex but "how to do math. like actually compute it"
    # is impossible to google for a language built to print math in pretty ways
    if render_settings is None:
        render_settings = RenderSettings()
    black = (0, 0, 0)
    first_black_step = 3
    if steps_in >= first_black_step:
        current_color = black
    else:
        # current_color = tuple([int(band * pow(0.5, steps_in)) for band in highlight_color])
        current_color = colors.mergecolors(render_settings.primary_color, render_settings.secondary_color,
                                           steps_in / (first_black_step - 1))
        # current_color = tuple(
        #     [int(band / first_black_step * (first_black_step - steps_in)) for band in highlight_color])
    final_color_string = colors.tuple_to_hex(current_color)
    return [
        rf"\fontsize{{{render_settings.text_curve_at(steps_in) * 0.75}mm}}{{{render_settings.text_curve_at(steps_in)}mm}}\selectfont",
        rf"\color[RGB]{{{str(current_color)[1:-1]}}}"
    ]


#        \fontsize{{{15 / (steps_in + 1)}mm }}{{{16 / (steps_in + 1)}mm}}\selectfont







@contextmanager
def tex_indent_context(latex_list: list[str]):
    latex_list.append(r"\begin{adjustwidth}{4mm}{}")
    latex_list.append("\n")
    yield latex_list
    latex_list.append(r"\end{adjustwidth}")


def tex_indent(latex_list: list[str]):
    new_list = []
    with tex_indent_context(new_list) as l:
        for n, x in enumerate(l):
            l[n] = "\t" + x
        l += latex_list
    return new_list


def import_all_classes():
    class_path = os.path.join(
        os.path.split(__file__)[0],
        "classes")
    for class_filename in os.listdir(class_path):
        class_name, _ = os.path.splitext(class_filename)
        importlib.import_module("_rg.classes." + class_name)
