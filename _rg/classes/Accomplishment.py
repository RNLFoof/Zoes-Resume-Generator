from pydantic import BaseModel, validator, Field

from _rg.classes.PotentialContent import PotentialContent
from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.Renderable import Renderable
from _rg.general import tex_change_emphasis, tex_header, tex_undivided_table, tex_escape


class Accomplishment(Renderable, BaseModel):
    name: str = Field(None, repr=False)
    description: str
    demonstrates: dict[str, str]

    def render(self, render_settings: RenderSettings) -> str:
        s = ""
        s += "{"
        s += tex_header(self.name, 2, render_settings, new_line=False)
        s += tex_change_emphasis(3)
        s += f"{self.description}\n\nMy work on this demonstrates..."
        for skill_name, because in self.demonstrates.items():
            s += "\n\n"
            s += fr"...\textit{{{tex_escape(skill_name)}}}: {tex_escape(because)}"
        s += "}\n\n"
        return s


class AccomplishmentSet(Renderable, PotentialContent):
    accomplishments: dict[str, Accomplishment]

    @validator('accomplishments')
    def __get_validators__(cls, accomplishments: dict[str, Accomplishment]):
        for name, accomplishment in accomplishments.items():
            accomplishment.name = name
        return accomplishments

    def render(self, render_settings: RenderSettings) -> str:
        s = ""
        s += "{"
        s += tex_header("Works", 1, render_settings)
        s += "\n\n".join([a.render(render_settings) for a in self.accomplishments.values()])
        s += "}"
        return s
