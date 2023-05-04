from pydantic import BaseModel, validator, Field

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.ChangeEmphasis import ChangeEmphasis
from _rg.classes.renderables.Heading import Heading
from _rg.classes.renderables.Indent import Indent
from _rg.classes.renderables.Renderable import Renderable
from _rg.classes.renderables.potential_content.PotentialContent import PotentialContent
from _rg.general import tex_escape


class Accomplishment(Renderable, BaseModel):
    name: str = Field(None, repr=False)
    description: str
    demonstrates: dict[str, str]

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [
            Heading(self.name, 2),
            ChangeEmphasis(3),
            self.description,
            "\nMy work on this demonstrates\\ldots",
            Indent([
                "\n" + fr"\ldots\textit{{{tex_escape(skill_name)}}}\: {tex_escape(because)}"
                for skill_name, because in self.demonstrates.items()
            ])
        ]


class AccomplishmentSet(PotentialContent):
    accomplishments: dict[str, Accomplishment]

    @validator('accomplishments')
    def __get_validators__(cls, accomplishments: dict[str, Accomplishment]):
        for name, accomplishment in accomplishments.items():
            accomplishment.name = name
        return accomplishments

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [Indent([
            Heading("Works", 1),
            Indent(
                list(self.accomplishments.values())
            )
        ])]
