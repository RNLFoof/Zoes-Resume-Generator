import typing
from typing import Union

from pydantic import BaseModel

from _rg.classes.Heading import Heading
from _rg.classes.PotentialContent import PotentialContent
from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.Renderable import RecursiveStrList, Renderable
from _rg.general import tex_change_emphasis, tex_indent


class HistoryItem(Renderable, BaseModel):
    name: str
    start_year: int
    end_year: Union[int | None]
    building: Union[str | None]

    def render(self, render_settings: RenderSettings) -> RecursiveStrList:
        return [self.name_tex(), self.date_tex()]

    def name_tex(self):
        if self.building is None:
            return self.name
        return fr"{{ {self.name} \\ {self.building} }}"

    def date_tex(self):
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

    def render(self, render_settings: RenderSettings) -> RecursiveStrList:
        return tex_indent([
            Heading("Education & Employment History", 1).render(render_settings),
            "\n",
            tex_change_emphasis(3),
            self.tex_table([e.render(render_settings) for e in self.all()], render_settings, horizontal_lines=True,
                           vertical_lines=True)
        ])
