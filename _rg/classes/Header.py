from _rg.classes.Heading import Heading
from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.Renderable import Renderable, RecursiveStrList
from _rg.general import tex_change_emphasis


class Header(Renderable):
    def render(self, render_settings: RenderSettings) -> RecursiveStrList:
        return self.tex_table(
            [
                [
                    r"\SetCell[r=2]{l}\includegraphics[width=24mm]{face}",
                    [r"\SetCell[c=3]{l}", Heading("Zoe Zablotsky", 0)],
                    "",
                    "",
                ],
                [
                    "",
                    [tex_change_emphasis(2), r"\href{mailto:z.zablotsky@gmail.com}{z.zablotsky@gmail.com}"],
                    "•",
                    r"\href{tel:+514-566-5567}{(514) 566\-5567}"
                ]
            ],
            render_settings)


"""\begin{adjustwidth}{4mm}{}
    \SetTblrInner{rowsep=0mm, leftsep=0mm, rightsep=4mm}
    \begin{tblr}{ llll }
        \SetCell[r=2]{l}
        \includegraphics[width=24mm]{face}
        &
        \SetCell[c=3]{l}
        __change_emphasis_to_0__
        __zoe__
        \\
        %(overwritten)
        &
        __change_emphasis_to_2__
        \SetCell{l}
        \href{mailto:z.zablotsky@gmail.com}{z.zablotsky@gmail.com}
        &
        \SetCell{l}
        •
        &
        \SetCell{l}
        \href{tel:+514-566-5567}{(514) 566-5567}
        \\
    \end{tblr}
\end{adjustwidth}"""
