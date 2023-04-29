from dataclasses import dataclass
from typing import Callable

from pydantic import BaseModel, validator
from pydantic import Field

from _rg.classes.Accomplishment import Accomplishment, AccomplishmentSet
from _rg.classes.Impressiveness import Impressiveness
from _rg.classes.PotentialContent import PotentialContent
from _rg.general import tex_escape


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


@dataclass
class SkillWithElaboration:
    skill: Skill
    relevant_accomplishments: list[Accomplishment]

    def tex(self):
        s = ""
        s += "{"
        s += self.skill.name
        s += "...\n\nAs demonstrated by my work on..."
        for accomplishment in self.relevant_accomplishments:
            relevance_phrasing = "because"
            explanation = accomplishment.demonstrates["GML"][relevance_phrasing]
            s += f"\n\n...GUY, {relevance_phrasing} {explanation}"
        s += "}"
        return s

class SkillSet(PotentialContent):
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

    @validator('skills')
    def __get_validators__(cls, skills: dict[str, Skill]):
        for name, skill in skills.items():
            skill.name = name

        return skills

    # TODO Perhaps this whole class should be a singleton, with this as a base.
    #  "all" in particular is a weird name for it at this point.

    def tex(self):
        s = ""

        s += SkillWithElaboration(
            self.skills["Game Maker Language"],
            [AccomplishmentSet.summon().accomplishments["Golf 2"]]).tex()

        columns = 2
        index = 0
        skills = self.skills_by_generic_value()
        while index <= len(skills) - columns:
            s += " & ".join([tex_escape(skill.name) for skill in skills[index:index + columns]])
            s += r"\\" + "\n"
            index += columns
        return s

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
