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
