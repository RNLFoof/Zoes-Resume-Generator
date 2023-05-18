import typing
from typing import Union

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.ChangeEmphasis import ChangeEmphasis
from _rg.classes.renderables.Demonstrable import Demonsterable
from _rg.classes.renderables.Heading import Heading
from _rg.classes.renderables.Indent import Indent
from _rg.classes.renderables.Renderable import Renderable
from _rg.classes.renderables.Table import Table
from _rg.classes.renderables.potential_content.PotentialContent import PotentialContent
from _rg.general import tex_escape


class HistoryItem(Renderable, BaseModel):
    name: str
    start_year: int
    end_year: Union[int | None]
    building: Union[str | None]
    building_formerly: Union[str | None]

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [
            Heading(tex_escape(self.name), 2),
            ChangeEmphasis(3),
            self.description(),
            "\n"
        ]

    def description(self) -> str:
        s = ""
        if self.building is not None:
            s += f"{self.building}, "
        return s

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

    def description(self) -> str:
        s = super().description()
        s += f"{self.completion_description} in {self.end_year}"
        return s

class DailyTask(Demonsterable):
    def begining(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [r"\ldots"] + super().begining(render_settings)
    def segway(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [r", which demonstrates\ldots"]

class Job(HistoryItem):
    daily_tasks: list[DailyTask]
    def description(self) -> str:
        s = super().description()
        s += self.timespan()
        return s

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return super().class_specific_render(render_settings) + [

                r"My daily tasks included\ldots",
                Indent(
                    list(self.daily_tasks)
                )
        ]

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
