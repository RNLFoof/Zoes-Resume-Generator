import typing
from typing import Union

from pydantic import BaseModel

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.ChangeEmphasis import ChangeEmphasis
from _rg.classes.renderables.Heading import Heading
from _rg.classes.renderables.Indent import Indent
from _rg.classes.renderables.Renderable import Renderable
from _rg.classes.renderables.Table import Table
from _rg.classes.renderables.potential_content.PotentialContent import PotentialContent


class HistoryItem(Renderable, BaseModel):
    name: str
    start_year: int
    end_year: Union[int | None]
    building: Union[str | None]

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [
            Heading(self.name, 2),
            ChangeEmphasis(3),
            self.timespan(),
            "\n"
        ]

    def name_tex(self) -> str:
        if self.building is None:
            return self.name
        return fr"{{ {self.name} \\ {self.building} }}"

    def timespan(self) -> str:
        if self.end_year is None:
            end = "Current"
        else:
            end = self.end_year
        if self.start_year == end:
            return str(end)
        return fr"{self.start_year}–{end}"


class Education(HistoryItem):
    completion_description: str


class Job(HistoryItem):
    pass


class History(PotentialContent):
    jobs: list[Job]
    education: list[Education]

    def all(self) -> list[HistoryItem]:
        return typing.cast(list[HistoryItem], self.jobs) + \
            typing.cast(list[HistoryItem], self.education)

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [
            Heading("Education & Employment History", 1),
            Indent(
                self.all()
            )
        ]
