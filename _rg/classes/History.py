from typing import Union, Any

import json5
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


history = None


class History(PotentialContent):
    jobs: list[Job]
    education: list[Education]

    def __init__(self, **data: Any):
        if history is not None:
            raise Exception("Already initialized! Access though History.history instead of History.History().")
        super().__init__(**data)

    def all(self) -> list[HistoryItem]:
        return self.jobs + self.education

    def tex(self):
        return "\n\hline\n".join([""] + [e.tex() for e in history.all()] + [""])


with open(History.SAVED_TO, "rb") as f:
    history = History(**json5.load(f))