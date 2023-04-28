from pydantic import BaseModel

from _rg.classes.PotentialContent import PotentialContent


class Accomplishment(BaseModel):
    description: str
    demonstrates: dict[str, dict[str, str]]


class AccomplishmentSet(PotentialContent):
    accomplishments: dict[str, Accomplishment]
