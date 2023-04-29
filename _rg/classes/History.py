import typing
from typing import Union

from pydantic import BaseModel

from _rg.classes.PotentialContent import PotentialContent


class HistoryItem(BaseModel):
    name: str
    start_year: int
    end_year: Union[int | None]
    building: Union[str | None]

    def tex(self):
        return fr"{self.name_tex()} & {self.date_tex()}\\"

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
            return end
        return f"{self.start_year}-{end}"


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

    def tex(self):
        return "\n\hline\n".join([""] + [e.tex() for e in self.all()] + [""])
