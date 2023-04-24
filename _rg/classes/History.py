import os
from typing import Iterable, ClassVar, Union

from pydantic import BaseModel


class HistoryItem(BaseModel):
    name: str
    start_year: int
    end_year: Union[int | None]


class Education(HistoryItem):
    completion_description: str


class Job(HistoryItem):
    pass


class History(BaseModel):
    jobs: Iterable[Job]
    education: Iterable[Education]

    SAVED_TO: ClassVar[str] = os.path.join(
        os.path.abspath(os.path.split(__file__)[0]),
        "../data/history.json5"
    )
    SCHEMA_SAVED_TO: ClassVar[str] = os.path.join(
        os.path.abspath(os.path.split(__file__)[0]),
        "../schema/history.json"
    )

    @classmethod
    def _dump_schema(cls) -> None:
        """Updates the schema used to validate the skill set provided in data/skillSet.json5."""
        with open(cls.SCHEMA_SAVED_TO, "w") as f:
            f.write(cls.schema_json(indent=4))


History._dump_schema()
