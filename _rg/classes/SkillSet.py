from dataclasses import dataclass
from typing import Callable

from pydantic import BaseModel, validator
from pydantic import Field

from _rg.classes.Accomplishment import Accomplishment, AccomplishmentSet
from _rg.classes.Heading import Heading
from _rg.classes.Impressiveness import Impressiveness
from _rg.classes.PotentialContent import PotentialContent
from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.Renderable import Renderable, RecursiveStrList
from _rg.general import tex_escape, tex_change_emphasis, tex_indent


class Skill(Renderable, BaseModel):
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

    def render(self, render_settings: RenderSettings) -> RecursiveStrList:
        return [tex_escape(self.name)]


@dataclass
class SkillWithElaboration:
    skill: Skill
    relevant_accomplishments: list[Accomplishment]

    def tex(self):
        s = ""
        s += "{"
        s += tex_change_emphasis(2)
        s += self.skill.name
        s += tex_change_emphasis(3)
        s += "\nAs demonstrated by my work on\ldots"
        for accomplishment in self.relevant_accomplishments:
            explanation = accomplishment.demonstrates[self.skill.name]
            s += f"\n\ldotsGUY{tex_change_emphasis(4)}({accomplishment.description}),{tex_change_emphasis(3)}\n\nbecause {explanation}"
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

    def render(self, render_settings: RenderSettings, elaborate=False) -> RecursiveStrList:
        columns = 2
        target_row = []
        skill_table = [target_row]
        skills_with_elaboration = {skill.name: SkillWithElaboration(skill, [])
                                   for skill in SkillSet.summon().skills_by_generic_value()}
        if elaborate:
            for name, accomplishment in AccomplishmentSet.summon().accomplishments.items():
                for skill in accomplishment.demonstrates.keys():
                    if skill in skills_with_elaboration:
                        skills_with_elaboration[skill].relevant_accomplishments.append(accomplishment)

        for skill_with_elaboration in skills_with_elaboration.values():
            skill = skill_with_elaboration.skill
            elaboration = skill_with_elaboration.relevant_accomplishments
            if len(elaboration) == 0:
                target_row.append(skill)
                if len(target_row) == columns:
                    target_row = []
                    skill_table.append(target_row)
            else:
                skill_table.append(skill_with_elaboration)
        if not skill_table[-1]:
            skill_table = skill_table[:-1]

        return [
            tex_indent([
                Heading("Skills", 1).render(render_settings),
                tex_change_emphasis(2),
                tex_indent(
                    self.tex_table(skill_table, render_settings)
                )
            ])
        ]

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
