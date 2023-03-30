from typing import Callable, Generator, List

import json5
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

SAVED_TO = "data/skillset.json5"
SCHEMA_SAVED_TO = "schema/skillset.json"


@dataclass
class Skill:
    impressiveness: float
    competence: float

    def generic_value(self):
        return self.impressiveness * self.competence


class Skillset(BaseModel):
    skills: dict[str, Skill]

    @classmethod
    def dump_schema(cls):
        with open(SCHEMA_SAVED_TO, "w") as f:
            f.write(cls.schema_json(indent=4))

    @classmethod
    def all(cls):
        with open(SAVED_TO, "rb") as f:
            return Skillset(**json5.load(f))

    def _skills_by(self, key: Callable[[(str, Skill)], any]) -> list[str]:
        return sorted(self.skills.items(), key=lambda x: key(x))

    def skills_by_generic_value(self):
        return self._skills_by(lambda i: -i[1].generic_value())
