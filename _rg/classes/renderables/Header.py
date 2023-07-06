import pathlib

from _rg.classes.RenderSettings import RenderSettings, RenderMode
from _rg.classes.renderables.IconLink import IconLink
from _rg.classes.renderables.WithEmphasis import WithEmphasis
from _rg.classes.renderables.Concatenate import Concatenate
from _rg.classes.renderables.Heading import Heading
from _rg.classes.renderables.Renderable import Renderable
from _rg.classes.renderables.Table import Table
from _rg.definitions import IMAGE_DIR


class Header(Renderable):
    # TODO these should all be in render settingds
    name = "Zoe Zablotsky"
    links = [
        "https://github.com/RNLFoof",
        "https://www.linkedin.com/in/zoe-zablotsky-598b2018a/"
    ]
    email = "z.zablotsky@gmail.com"
    phone_number = "514-566-5567"
    # TODO these two should be functions
    phone_number_for_href = "tel:+514-566-5567"
    phone_number_for_display = "(514) 566\-5567"
    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        if render_settings.render_mode == RenderMode.PDF:
            return [
                Table(
                    [
                        [
                            r"\SetCell[r=2]{l}\includegraphics[width=24mm]{face}",
                            Concatenate([
                                r"\SetCell[c=3]{l}",
                                Heading(self.name, 0)
                            ]),
                            "",
                            "",
                            Concatenate([
                                r"\SetCell[r=2]{r}",
                                WithEmphasis(3, [
                                    Table(
                                        [
                                            [
                                                IconLink("https://github.com/RNLFoof")
                                            ],
                                            [
                                                IconLink("https://www.linkedin.com/in/zoe-zablotsky-598b2018a/")
                                            ]
                                        ]
                                    )
                                ])
                            ])

                        ],
                        [
                            "",
                            WithEmphasis(2, [r"\href{mailto:z.zablotsky@gmail.com}{z.zablotsky@gmail.com}"]),
                            WithEmphasis(2, ["•"]),
                            WithEmphasis(2, [r"\href{tel:+514-566-5567}{(514) 566\-5567}"]),
                            ""
                        ]
                    ]
                , table_params={
                        "width": r"\linewidth",
                        "colspec": r"lllX[l]l"
                    })
            ]
        else:
            return [self.name, self.email, self.phone_number] + self.links
