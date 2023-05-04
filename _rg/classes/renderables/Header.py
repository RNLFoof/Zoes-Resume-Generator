from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.ChangeEmphasis import ChangeEmphasis
from _rg.classes.renderables.Heading import Heading
from _rg.classes.renderables.Renderable import Renderable
from _rg.classes.renderables.Table import Table


class Header(Renderable):
    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [
            Table(
                [
                    [
                        r"\SetCell[r=2]{l}\includegraphics[width=24mm]{face}",
                        r"\SetCell[c=3]{l}" + Heading("Zoe Zablotsky", 0).render_wrapper(render_settings),
                        # TODO Should have some way to concat
                        "",
                        "",
                    ],
                    [
                        "",
                        ChangeEmphasis(2).render_wrapper(
                            render_settings) + r"\href{mailto:z.zablotsky@gmail.com}{z.zablotsky@gmail.com}",
                        # TODO Should have some way to concat
                        "•",
                        r"\href{tel:+514-566-5567}{(514) 566\-5567}"
                    ]
                ]
            )
        ]
