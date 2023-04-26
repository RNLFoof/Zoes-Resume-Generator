from pydantic import BaseModel


class Accomplishment(BaseModel):
    description: str
    demonstrates: dict[str, dict[str, str]]


class AccomplishmentSet(BaseModel):
    accomplishments: dict[str, Accomplishment]
