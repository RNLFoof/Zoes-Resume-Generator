import pathlib

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.WithEmphasis import WithEmphasis
from _rg.classes.renderables.Concatenate import Concatenate
from _rg.classes.renderables.Heading import Heading
from _rg.classes.renderables.Renderable import Renderable
from _rg.classes.renderables.Table import Table
from _rg.definitions import IMAGE_DIR


class Header(Renderable):
    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [
            Table(
                [
                    [
                        r"\SetCell[r=2]{l}\includegraphics[width=24mm]{face}",
                        Concatenate([
                            r"\SetCell[c=3]{l}",
                            Heading("Zoe Zablotsky", 0)
                        ]),
                        "",
                        "",
                    ],
                    [
                        "",
                        WithEmphasis(2, [r"\href{mailto:z.zablotsky@gmail.com}{z.zablotsky@gmail.com}"]),
                        WithEmphasis(2, ["•"]),
                        WithEmphasis(2, [r"\href{tel:+514-566-5567}{(514) 566\-5567}"]),
                    ]
                ]
            )
        ]
