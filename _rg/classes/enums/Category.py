from enum import Enum, auto
from typing import Any, Optional, Self


class Category(Enum):
    """

    """

    def __init__(self, number: int, display_name_overwrite: Optional[str] = None,
                 subcategory_of: Optional[Self] = None):
        self.number = number
        self.display_name_overwrite = display_name_overwrite
        self.subcategory_of = subcategory_of

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]):
        """Method used by Pydantic to modify how Category is serialized.

        In particular, replaces the description with one not tainted with Python documentation,
        and uses Category's names instead of its significantly more unwieldy values.

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

        In particular, takes the Enum name, or an actual Category instance, instead of value.
        """

        def validators(value: str | Category):
            if type(value) is str:
                return cls[value]
            if type(value) is Category:
                return value

        yield lambda value: validators(value)

    def display_name(self):
        if self.display_name_overwrite:
            return self.display_name_overwrite
        return self.name.replace("_", " ").title()

    PROGRAMMING = auto()
    THREED_MODELING = auto(), "3D Modeling and Printing"
    OFFICE_SOFTWARE = auto()
    MISCELLANEOUS = auto()
