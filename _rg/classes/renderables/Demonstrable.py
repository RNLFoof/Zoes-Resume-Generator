
from pydantic import BaseModel, Field, validator

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.ChangeEmphasis import ChangeEmphasis
from _rg.classes.renderables.Concatenate import Concatenate
from _rg.classes.renderables.Heading import Heading
from _rg.classes.renderables.Indent import Indent
from _rg.classes.renderables.Renderable import Renderable
from _rg.general import tex_escape


class Demonsterable(Renderable, BaseModel):
    description: str
    demonstrates: dict[str, str | None]

    class Config:
        # A little silly. https://github.com/pydantic/pydantic/issues/5755
        @staticmethod
        def schema_extra(schema: dict[str, ...]):
            schema.setdefault("properties", {}) \
                .setdefault("demonstrates", {}) \
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


    # @staticmethod
    @validator('demonstrates')
    def default_demonstration_description(value: dict[str | None]) -> dict[str, str]:
        from _rg.classes.renderables.potential_content.SkillSet import SkillSet
        for k, v in value.items():
            if v is None:
                value[k] = SkillSet.summon().skills[k].default_usage
        return value

    def begining(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [
            ChangeEmphasis(3),
            self.description
        ]

    def segway(self, render_settings: RenderSettings) -> list[str | Renderable]:
        raise NotImplemented()

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return self.begining(render_settings) + \
            self.segway(render_settings) + \
        [

            Indent([
                Concatenate(
                    [ChangeEmphasis(3)] +
                    [
                        fr"\ldots\textit{{{tex_escape(skill_name)}}}: {tex_escape(because)}" + "\n"
                        for skill_name, because in self.demonstrates.items()
                    ])
            ])
        ]