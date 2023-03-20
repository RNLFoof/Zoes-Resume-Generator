import json5
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

SAVED_TO = "data/skillset.json5"
SCHEMA_SAVED_TO = "schema/skillset.json"


@dataclass
class Skill:
    impressiveness: float
    competence: float


class Skillset(BaseModel):
    skills: dict[str, Skill]

    @classmethod
    def dump_schema(cls):
        with open(SCHEMA_SAVED_TO, "w") as f:
            f.write(cls.schema_json())

    @classmethod
    def all(cls):
        with open(SAVED_TO, "rb") as f:
            return Skillset(**json5.load(f))
