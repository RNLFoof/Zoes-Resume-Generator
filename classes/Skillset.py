import os
from typing import Callable

import json5
from pydantic import BaseModel

from Impressiveness import Impressiveness

SAVED_TO = os.path.join(
    os.path.abspath(os.path.split(__file__)[0]),
    "../data/skillset.json5"
)
SCHEMA_SAVED_TO = os.path.join(
    os.path.abspath(os.path.split(__file__)[0]),
    "../schema/skillset.json"
)


class Skill(BaseModel):
    competence: float
    impressiveness: Impressiveness

    def generic_value(self):
        return self.impressiveness.value * self.competence


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
