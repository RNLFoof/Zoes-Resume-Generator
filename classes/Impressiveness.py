from enum import Enum


class Impressiveness(Enum):
    """Enum for expressing the impressiveness of a skill. That is, how much talent or knowledge goes into it.

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

    NONE = 0, "Useless garbage"

    SIMPLE = 1, """ 
        Could be learned in its entirety in a day and has no real edges
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

    DEEP = 3, "Has depth"

    MAKE_OR_BREAK = 4, "Could be a make or break skill for a position"

    SPECIALIZABLE = 5, "Somebody could specialize in this"
