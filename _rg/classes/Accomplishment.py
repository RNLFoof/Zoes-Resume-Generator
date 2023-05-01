from pydantic import BaseModel, validator, Field

from _rg.classes.PotentialContent import PotentialContent
from _rg.general import tex_change_emphasis


class Accomplishment(BaseModel):
    name: str = Field(None, repr=False)
    description: str
    demonstrates: dict[str, str]


class AccomplishmentSet(PotentialContent):
    accomplishments: dict[str, Accomplishment]

    @validator('accomplishments')
    def __get_validators__(cls, accomplishments: dict[str, Accomplishment]):
        for name, accomplishment in accomplishments.items():
            accomplishment.name = name
        return accomplishments

    def tex(self):
        s = ""
        for accomplishment in self.accomplishments.values():
            s += tex_change_emphasis(2)
            s += accomplishment.name
            s += tex_change_emphasis(3)
            s += f"({accomplishment.description})"
            s += "\n\n"
        return s
