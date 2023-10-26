import typing
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from typing import Union

from _rg.classes.RenderSettings import RenderSettings, RenderFormat
from _rg.classes.renderables.Demonstrable import Demonsterable
from _rg.classes.renderables.Heading import Heading
from _rg.classes.renderables.Indent import Indent
from _rg.classes.renderables.Renderable import Renderable
from _rg.classes.renderables.Table import Table
from _rg.classes.renderables.WithEmphasis import WithEmphasis
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
            WithEmphasis(3, [self.description(render_settings)], no_break=True),
            "\n"
        ]

    def description(self, render_settings: RenderSettings) -> str:
        s = ""
        if self.building is not None:
            s += f"{self.building}"

            if render_settings.render_format != RenderFormat.INDEED_HTML:
                s += ", "

        return s

    def timespan(self, render_settings: RenderSettings) -> str:
        if self.end_year is None:
            end = "Present"
        else:
            end = self.end_year
        if self.start_year == end:
            return str(end)

        if render_settings.render_format in [RenderFormat.MARKDOWN, RenderFormat.INDEED_HTML]:
            seprator = " to "
        else:
            seprator = "-"

        return fr"{self.start_year}{seprator}{end}"


class Education(HistoryItem):
    completion_description: str

    def description(self, render_settings: RenderSettings) -> str:
        if render_settings.render_format == RenderFormat.INDEED_HTML:
            return [f"{self.completion_description} {self.name}", self.building, self.timespan(render_settings)]

        s = super().description(render_settings)
        s += f"{self.completion_description} in {self.end_year}"
        return s

class DailyTask(Demonsterable):
    def begining(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [r"$\smallblacksquare$"] + super().begining(render_settings)
    def segway(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [r", which demonstrates:"]

class Job(HistoryItem):
    daily_tasks: list[DailyTask]

    def description(self, render_settings: RenderSettings) -> str:

        s = super().description(render_settings)

        if render_settings.render_format == RenderFormat.INDEED_HTML:
            s += "\n"

        s += self.timespan(render_settings)
        return s

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        if render_settings.render_format in [RenderFormat.MARKDOWN, RenderFormat.INDEED_HTML]:
            return super().class_specific_render(render_settings)

        return [WithEmphasis(3,
                    super().class_specific_render(render_settings) + [
                    r"My daily tasks included:",
                    Indent(
                        list(self.daily_tasks)
                    )
        ])]


class History(PotentialContent):
    jobs: list[Job]
    education: list[Education]

    def all(self) -> list[HistoryItem]:
        return typing.cast(list[HistoryItem], self.jobs) + \
            typing.cast(list[HistoryItem], self.education)

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        if render_settings.render_format in [RenderFormat.INDEED_HTML]:
            return [WithEmphasis(2, [
                Heading("Work Experience", 1),
                Indent(
                    self.jobs
                ),
            ])]

        else:
            return [WithEmphasis(2, [
                Heading("Work Experience", 1),
                Indent(
                    self.jobs
                ),
                Heading("Education", 1),
                Indent(
                    self.education
                )
            ])]
