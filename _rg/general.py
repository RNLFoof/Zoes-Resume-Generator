import re

from zsil import colors

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.Renderable import Renderable


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
    return rf"""
        \definecolor{{temp}}{{HTML}}{{{final_color_string}}}\
        \fontsize{{{render_settings.largest_text_size * pow(0.5, steps_in) * 0.75}mm }}{{{render_settings.largest_text_size * pow(0.5, steps_in)}mm}}\selectfont
        \color{{temp}}
    """.strip()


#        \fontsize{{{15 / (steps_in + 1)}mm }}{{{16 / (steps_in + 1)}mm}}\selectfont

def tex_header(text: str, steps_in: int, render_settings: RenderSettings, new_line=True):
    s = "{"
    s += tex_change_emphasis(steps_in)
    if render_settings.title_gradients:
        for letter_index, letter in enumerate(text):
            text_progress = letter_index / (len(text) - 1)
            current_color = colors.mergecolors(render_settings.start_color_at(steps_in),
                                               render_settings.secondary_color,
                                               text_progress)
            s += fr"\color[RGB]{{{str(current_color)[1:-1]}}}{{{letter}}}"
    else:
        s += text
    s += "}"

    if new_line:
        s += r"\\"

    return s


def tex_undivided_table(table: list[list[Renderable]], render_settings: RenderSettings):
    s = ""
    column_count = max(len(row) for row in table)
    s += rf"""\SetTblrInner{{rowsep=0mm, leftsep=1mm, rightsep=4mm}}
        \begin{{tblr}}{{ {"l" * column_count} }}"""

    for row in table:
        if len(row) == column_count:
            s += " & ".join([cell.render(render_settings) for cell in row])
        elif len(row) == 1:
            s += fr"\SetCell[c={column_count}]{{l}}" + row[0].render()
        else:
            raise NotImplementedError()
        s += r"\\" + "\n"

    s += """"\end{tblr}"""
    return s
