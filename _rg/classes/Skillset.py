import os
from typing import Callable

import json5
from pydantic import BaseModel

from _rg.classes.Impressiveness import Impressiveness

SAVED_TO = os.path.join(
    os.path.abspath(os.path.split(__file__)[0]),
    "../data/skillSet.json5"
)
SCHEMA_SAVED_TO = os.path.join(
    os.path.abspath(os.path.split(__file__)[0]),
    "../schema/skillSet.json"
)


class Skill(BaseModel):
    """Represents a skill. That is, a thing that I (know|could know) how to (do|use|write in).

    Parameters
    ----------
    competence : float
        Numerical value representing how good Zoe is at this skill.
    impressiveness : Impressiveness
        Impressiveness value associated with this skill.

    See Also
    --------
    Impressiveness.Impressiveness
    """
    competence: float
    impressiveness: Impressiveness

    def generic_value(self):
        return self.impressiveness.number * self.competence


class SkillSet(BaseModel):
    """

    """
    skills: dict[str, Skill]

    @classmethod
    def dump_schema(cls):
        with open(SCHEMA_SAVED_TO, "w") as f:
            f.write(cls.schema_json(indent=4))

    @classmethod
    def all(cls):
        with open(SAVED_TO, "rb") as f:
            return SkillSet(**json5.load(f))

    def _skills_by(self, key: Callable[[(str, Skill)], any]) -> list[str]:
        return sorted(self.skills.items(), key=lambda x: key(x))

    def skills_by_generic_value(self):
        return self._skills_by(lambda i: -i[1].generic_value())
