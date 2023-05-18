from pydantic import BaseModel, validator, Field

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.ChangeEmphasis import ChangeEmphasis
from _rg.classes.renderables.Concatenate import Concatenate
from _rg.classes.renderables.Demonstrable import Demonsterable
from _rg.classes.renderables.Heading import Heading
from _rg.classes.renderables.Indent import Indent
from _rg.classes.renderables.Renderable import Renderable
from _rg.classes.renderables.potential_content.PotentialContent import PotentialContent
from _rg.general import tex_escape


class Work(Demonsterable):
    name: str = Field(None, repr=False)

    def begining(self, render_settings: RenderSettings):
        return [
            Heading(self.name, 2)
        ] + super().begining(render_settings)

    def segway(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return ["\nMy work on this demonstrates\\ldots"]

class BodyOfWork(PotentialContent):
    works: dict[str, Work]

    @validator('works')
    def __get_validators__(cls, works: dict[str, Work]):
        for name, accomplishment in works.items():
            accomplishment.name = name
        return works

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [Indent([
            Heading("Works", 1),
            Indent(
                list(self.works.values())
            )
        ])]
