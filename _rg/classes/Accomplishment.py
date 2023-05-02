from pydantic import BaseModel, validator, Field

from _rg.classes.PotentialContent import PotentialContent
from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.Renderable import Renderable
from _rg.general import tex_change_emphasis, tex_header, tex_escape


class Accomplishment(Renderable, BaseModel):
    name: str = Field(None, repr=False)
    description: str
    demonstrates: dict[str, str]

    def render(self, render_settings: RenderSettings) -> list[str]:
        return [
            "{",
            tex_header(self.name, 2, render_settings, new_line=False),
            tex_change_emphasis(3),
            f"{self.description}\n\nMy work on this demonstrates...",
        ] + [
            "\n\n" + fr"...\textit{{{tex_escape(skill_name)}}}: {tex_escape(because)}"
            for skill_name, because in self.demonstrates.items()
        ] + [
            "}\n\n"
        ]


class AccomplishmentSet(Renderable, PotentialContent):
    accomplishments: dict[str, Accomplishment]

    @validator('accomplishments')
    def __get_validators__(cls, accomplishments: dict[str, Accomplishment]):
        for name, accomplishment in accomplishments.items():
            accomplishment.name = name
        return accomplishments

    def render(self, render_settings: RenderSettings) -> list[str]:
        return [
            "{",
            tex_header("Works", 1, render_settings),
            "\n\n".join([a.render_as_string(render_settings) for a in self.accomplishments.values()]),
            "}"
        ]
