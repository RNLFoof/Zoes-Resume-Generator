from dataclasses import dataclass
from typing import Callable, Optional

from pydantic import BaseModel, validator
from pydantic import Field

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.enums.Category import Category
from _rg.classes.enums.Impressiveness import Impressiveness
from _rg.classes.renderables.WithEmphasis import WithEmphasis
from _rg.classes.renderables.Heading import Heading
from _rg.classes.renderables.Indent import Indent
from _rg.classes.renderables.Renderable import Renderable
from _rg.classes.renderables.Table import Table
from _rg.classes.renderables.potential_content.BodyOfWork import Work, BodyOfWork
from _rg.classes.renderables.potential_content.PotentialContent import PotentialContent
from _rg.general import tex_escape


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
    category: Category
    default_usage_overwrite: Optional[str] = Field(None, alias="default_usage")

    def generic_value(self) -> float:
        """Numeric value of this skill, independent on any specific job posting or intent.

        Returns
        -------
        float
            Said numerical value.
        """
        return self.impressiveness.number * self.competence

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [tex_escape(self.name)]

    @property
    def default_usage(self) -> str:
        if self.default_usage_overwrite is not None:
            return self.default_usage_overwrite
        return self.category.default_usage


@dataclass
class SkillWithElaboration:
    skill: Skill
    relevant_works: list[Work]

    def tex(self):
        s = ""
        s += "{"
        s += WithEmphasis(2)
        s += self.skill.name
        s += WithEmphasis(3)
        s += "\nAs demonstrated by my work on:"
        for accomplishment in self.relevant_works:
            explanation = accomplishment.demonstrates[self.skill.name]
            s += f"\n$\$\smallblacksquare$$GUY{WithEmphasis(4)}({accomplishment.description}),{WithEmphasis(3)}\n\nbecause {explanation}"
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

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        @dataclass
        class TableForCategory:
            target_row: list[str | Renderable]
            content: list[list[str | Renderable]]

        tables_for_categories: dict[str, TableForCategory] = {}
        skills_with_elaboration = {skill.name: SkillWithElaboration(skill, [])
                                   for skill in SkillSet.summon().skills_by_generic_value()}
        if render_settings.skill_elaboration:
            for name, accomplishment in BodyOfWork.summon().works.items():
                for skill in accomplishment.demonstrates.keys():
                    if skill in skills_with_elaboration:
                        skills_with_elaboration[skill].relevant_works.append(accomplishment)

        for skill_with_elaboration in skills_with_elaboration.values():
            skill = skill_with_elaboration.skill
            elaboration = skill_with_elaboration.relevant_works

            key = skill.category.display_name() if render_settings.show_categories else "burp"
            if key not in tables_for_categories:
                tables_for_categories[key] = TableForCategory(
                    target_row := [],
                    [target_row]
                )
            tfc = tables_for_categories[key]

            if len(elaboration) == 0:
                tfc.target_row.append(skill)
                if len(tfc.target_row) == render_settings.skill_columns:
                    tfc.target_row = []
                    tfc.content.append(tfc.target_row)
            else:
                tfc.content.append(skill_with_elaboration)
        for tfc in tables_for_categories.values():
            if not tfc.content[-1]:
                tfc.content.pop(-1)

        if render_settings.show_categories:
            the_important_bit = [
                Indent([
                    Heading(category_name, 2),
                    Indent([
                        WithEmphasis(3, [
                            Table(tfc.content)
                        ])
                    ])
                ])
                for category_name, tfc in tables_for_categories.items()
            ]
        else:
            the_important_bit = [
                WithEmphasis(3, [
                    Indent([
                        Table(list(tables_for_categories.values())[0].content)
                    ])
                ]),
            ]
        return [
            Indent([
                       Heading("Skills", 1)
                   ] + the_important_bit
                   )
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
