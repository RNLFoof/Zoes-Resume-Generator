from pydantic import BaseModel, validator, Field

from _rg.classes.Header import Header
from _rg.classes.PotentialContent import PotentialContent
from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.Renderable import Renderable, RecursiveStrList
from _rg.general import tex_change_emphasis, tex_escape, tex_indent


class Accomplishment(Renderable, BaseModel):
    name: str = Field(None, repr=False)
    description: str
    demonstrates: dict[str, str]

    def render(self, render_settings: RenderSettings) -> RecursiveStrList:
        return [
            Header(self.name, 2).render(render_settings),
            tex_change_emphasis(3),
            self.description,
            "\n\nMy work on this demonstrates\\ldots",
            tex_indent([
                "\n\n" + fr"\ldots\textit{{{tex_escape(skill_name)}}}: {tex_escape(because)}"
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

    def render(self, render_settings: RenderSettings) -> RecursiveStrList:
        return [
            Header("Works", 1).render(render_settings),
            tex_indent(
                "\n\n".join([a.render_as_string(render_settings) for a in self.accomplishments.values()])
            )
        ]
