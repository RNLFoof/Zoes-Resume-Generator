import re


def tex_escape(text: str) -> str:
    text = text.replace("\\", r"\textbackslash")
    text = re.sub(r"([&%$#_{}])", r"\\\1", text)
    text = text.replace("~", r"\textasciitilde")
    text = text.replace("^", r"\textasciicircum")
    return text


def tex_change_emphasis(steps_in: int):
    # TODO There's absolutely a way to do this within the bounds of latex but "how to do math. like actually compute it"
    # is impossible to google for a language built to print math in pretty ways
    highlight_color = (0x00, 0xa0, 0xa0)
    black = (0, 0, 0)
    steps_to_black = 3
    if steps_in >= steps_to_black:
        current_color = black
    else:
        # current_color = tuple([int(band * pow(0.5, steps_in)) for band in highlight_color])
        current_color = tuple(
            [int(band / steps_to_black * (steps_to_black - steps_in / 2)) for band in highlight_color])
    final_color_string = "".join([f"{x:x}".ljust(2, "0") for x in current_color])
    return rf"""
        \definecolor{{temp}}{{HTML}}{{{final_color_string}}}
        \fontsize{{{15 / (steps_in + 1)}mm }}{{{16 / (steps_in + 1)}mm}}\selectfont
        \color{{temp}}
    """.strip()
#        \fontsize{{{15 * pow(0.5, steps_in)}mm }}{{{16 * pow(0.5, steps_in)}mm}}\selectfont
