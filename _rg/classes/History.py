import os
from typing import ClassVar, Union, Any

import json5
from pydantic import BaseModel


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


class History(BaseModel):
    jobs: list[Job]
    education: list[Education]

    SAVED_TO: ClassVar[str] = os.path.join(
        os.path.abspath(os.path.split(__file__)[0]),
        "../data/history.json5"
    )
    SCHEMA_SAVED_TO: ClassVar[str] = os.path.join(
        os.path.abspath(os.path.split(__file__)[0]),
        "../schema/history.json"
    )

    def __init__(self, **data: Any):
        if history is not None:
            raise Exception("Already initialized! Access though History.history instead of History.History().")
        super().__init__(**data)

    @classmethod
    def _dump_schema(cls) -> None:
        """Updates the schema used to validate the skill set provided in data/history.json5."""
        with open(cls.SCHEMA_SAVED_TO, "w") as f:
            f.write(cls.schema_json(indent=4))

    def all(self) -> list[HistoryItem]:
        return self.jobs + self.education

    def tex(self):
        return "\n\hline\n".join([""] + [e.tex() for e in history.all()] + [""])


with open(History.SAVED_TO, "rb") as f:
    history = History(**json5.load(f))

History._dump_schema()
