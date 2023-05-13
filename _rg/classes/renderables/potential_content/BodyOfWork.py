from pydantic import BaseModel, validator, Field

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.ChangeEmphasis import ChangeEmphasis
from _rg.classes.renderables.Concatenate import Concatenate
from _rg.classes.renderables.Heading import Heading
from _rg.classes.renderables.Indent import Indent
from _rg.classes.renderables.Renderable import Renderable
from _rg.classes.renderables.potential_content.PotentialContent import PotentialContent
from _rg.general import tex_escape


class Work(Renderable, BaseModel):
    name: str = Field(None, repr=False)
    description: str
    demonstrates: dict[str, str | None]

    class Config:
        # A little silly. https://github.com/pydantic/pydantic/issues/5755
        @staticmethod
        def schema_extra(schema: dict[str, ...]):
            schema.setdefault("properties", {})\
                .setdefault("demonstrates", {})\
                ["additionalProperties"] = {
                    "anyOf": [
                        {
                            "type": "string"
                        },
                        {
                            "type": "null"
                        }
                    ]
                }


    @validator('demonstrates')
    def default_demonstration_description(value: dict[str | None]) -> dict[str, str]:
        for k, v in value.items():
            if v is None:
                value[k] = "default"  # TODO this should actually be something useful
        return value

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [
            Heading(self.name, 2),
            ChangeEmphasis(3),
            self.description,
            "\nMy work on this demonstrates\\ldots",
            Indent([
                Concatenate(
                    [ChangeEmphasis(3)] +
                    [
                        fr"\ldots\textit{{{tex_escape(skill_name)}}}: {tex_escape(because)}" + "\n"
                        for skill_name, because in self.demonstrates.items()
                    ])
            ])
        ]


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
