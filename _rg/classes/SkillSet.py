import os
from typing import Callable, ClassVar

import json5
from pydantic import BaseModel, validator
from pydantic import Field

from _rg.classes.Impressiveness import Impressiveness


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
    Impressiveness.Impressiveness : Specificity on what each impressiveness value means.
    """
    name: str = Field(None, repr=False)
    competence: float
    impressiveness: Impressiveness

    def generic_value(self) -> float:
        """Numeric value of this skill, independent on any specific job posting or intent.

        Returns
        -------
        float
            Said numerical value.
        """
        return self.impressiveness.number * self.competence


class SkillSet(BaseModel):
    """Represents the list of skills with potential to go onto the resume.

    Parameters
    ----------
    skills : dict[str, Skill]
        Skills by name, not necessarily ones that Zoe has.

    See Also
    --------
    Skill : Specificity on what information is associated with a skill.
    """
    skills: dict[str, Skill]

    SAVED_TO: ClassVar[str] = os.path.join(
        os.path.abspath(os.path.split(__file__)[0]),
        "../data/skillSet.json5"
    )
    SCHEMA_SAVED_TO: ClassVar[str] = os.path.join(
        os.path.abspath(os.path.split(__file__)[0]),
        "../schema/skillSet.json"
    )

    @validator('skills')
    def __get_validators__(cls, skills: dict[str, Skill]):
        """
        """
        for name, skill in skills.items():
            skill.name = name

        return skills

    @classmethod
    def _dump_schema(cls) -> None:
        """Updates the schema used to validate the skill set provided in data/skillSet.json5."""
        with open(cls.SCHEMA_SAVED_TO, "w") as f:
            f.write(cls.schema_json(indent=4))

    # TODO Perhaps this whole class should be a singleton, with this as a base.
    #  "all" in particular is a weird name for it at this point.
    @classmethod
    def all(cls) -> "SkillSet":
        """Gets all the skills provided in data/skillSet.json5.

        Returns
        -------
        SkillSet
            SkillSet representing Zoe's skills (or lack thereof).
        """
        with open(cls.SAVED_TO, "rb") as f:
            return SkillSet(**json5.load(f))

    def _skills_by(self, key: Callable[[Skill], any]) -> list[Skill]:
        """A generic function for creating other functions that return the skills sorted in some way.

        Parameters
        ----------
        key : Callable[[Skill], any]
            Function that takes a skill and returns a value that can be sorted.

        Returns
        -------
        list[Skill]
            Skill names, sorted.
        """
        return sorted(self.skills.values(), key=lambda x: key(x))

    def skills_by_generic_value(self) -> list[Skill]:
        """All skill names, sorted by descending generic value.

        Returns
        -------
        list[Skill]
            I assume that you can infer from context.
        """
        return self._skills_by(lambda i: -i.generic_value())
