from enum import Enum
from typing import Any


class Impressiveness(Enum):
    """Enum for expressing the impressiveness of a skill.

    That is, how much talent or knowledge goes into it, or how challenging it is to learn or use.

    Parameters
    ----------
    number : float
        Numerical value used to weigh this skill. Very much based on gut feeling.
    description : str
        Clarification on what really fits this label.
    """

    def __init__(self, number: float, description: str):
        self.number = number
        self.description = description

    def __float__(self):
        return float(self.number)

    def __cmp__(self, other: "Impressiveness"):
        return self.number - other.number

    def __lt__(self, other: "Impressiveness"):
        return self.number < other.number

    def __gt__(self, other: "Impressiveness"):
        return self.number > other.number

    def __repr__(self):
        return f"Impressiveness.{self.name}"

    def __str__(self):
        return f"Impressiveness.{self.name}"

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]):
        """Method used by Pydantic to modify how Impressiveness is serialized.

        In particular, replaces the description with one not tainted with Python documentation,
        and uses Impressiveness' names instead of its significantly more unwieldy values.

        Parameters
        ----------
        field_schema : dict[str, Any]
            Otherwise complete schema for this type, provided by Pydantic, to be modified in place.
        """
        field_schema["description"] = cls.__doc__.splitlines()[0]  # TODO You can embed this into the field
        field_schema["enum"] = [item.name for item in cls]

    # Modified version of https://github.com/pydantic/pydantic/issues/598#issuecomment-503032706
    @classmethod
    def __get_validators__(cls):
        """Method used by Pydantic to modify how Impressiveness is deserialized.

        In particular, takes the Enum name, or an actual Impressiveness instance, instead of value.
        """

        def validators(value: str | Impressiveness):
            if type(value) is str:
                return cls[value]
            if type(value) is Impressiveness:
                return value

        yield lambda value: validators(value)

    @classmethod
    def lower_bound(cls) -> float:
        """The lowest possible numerical value that can be assigned to a skill.

        Returns
        -------
        float
            Said numerical value.
        """
        return min(item.number for item in cls)

    @classmethod
    def upper_bound(cls) -> float:
        """The highest possible numerical value that can be assigned to a skill.

        Returns
        -------
        float
            Said numerical value.
        """
        return max(item.number for item in cls)

    NONE = 0, "Useless garbage"

    SIMPLE = 1, """ 
        Could be learned in its entirety in a day, and has no real edges.
        Ex. JSON
    """

    INTUITIVE = 1.5, """
        You couldn't trivially memorize all of it, but you won't have any trouble learning how to do new things.
        Ex. Google Calendar, Hue Manager
    """

    INTUITIVE_WITH_CONTEXT = 1.75, """     
        Same as intuitive, but only if you have prior knowledge about some other thing.
        Ex. MSAL, which would be confusing if you knew nothing about authorization.
    """

    BEGINNER = 2, """     
        Deliberately simplified at the expense of otherwise expected functionality, but still versatile.
        Intended for people who don't know how to use better but more complicated tools.
        Ex. GML, Power Automate
    """

    EXPANSIVE = 2.5, """
        It's BIG. Can you explore it? Uh, kinda. You mostly just Google the thing you want to do.
        Ex. PyCharm
    """

    # TODO There's a few things with this label that don't fit this description.
    DEEP = 3, """
        Has some amount of explorable depth. Contrasts beginner, where once you go past the basics,
        you're mostly just trying to get around its limitations.
        Ex. Pillow, Regular Expressions, jQuery
    """

    # TODO This is more about how well it fits into a workplace than how challenging it is.
    MAKE_OR_BREAK = 4, """
        Can be so fundamental to a job that it can sway applicability on its own.
        Ex. Kotlin, Git, Django
    """

    # TODO Like DEEP, I think some of the things labelled as this don't fit.
    SPECIALIZABLE = 5, """
        Has so much going on that somebody could make a career on being really good at just this.
        Ex. C#, Javascript
    """
