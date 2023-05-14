from enum import Enum, auto
from typing import Any, Optional, Self


class Category(Enum):
    """

    """

    # TODO Config use_enum_values? https://docs.pydantic.dev/latest/usage/model_config/
    def __init__(self, number: int, default_usage: Optional[str], _display_name: Optional[str],
                 subcategory_of: Optional[Self]):
        self.number = number
        self._default_usage = default_usage
        self._display_name = _display_name
        self._subcategory_of = subcategory_of

    @staticmethod
    def init_wrapper(default_usage: Optional[str] = None, display_name: Optional[str] = None,
                     subcategory_of: Optional["Category"] = None):
        return auto(), default_usage, display_name, subcategory_of

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

    @property
    def display_name(self):
        if self._display_name:
            return self._display_name
        return self.name.replace("_", " ").title()

    @property
    def default_usage(self):
        if self._default_usage is not None:
            return self._default_usage
        if self.subcategory_of is not None:
            return self.subcategory_of.default_usage
        raise Exception("No default usage!")

    @property
    def subcategory_of(self):
        if self._subcategory_of is None:
            return None

        return [c for c in Category if c.value == self._subcategory_of][0]

    PROGRAMMING = init_wrapper(default_usage="That's what it's written in")
    THREED_MODELING = init_wrapper(default_usage="That's what it's modeled in",
                                   display_name="3D Modeling and Printing")
    OFFICE_SOFTWARE = init_wrapper()
    SHAREPOINT = init_wrapper(subcategory_of=OFFICE_SOFTWARE)
    MISCELLANEOUS = init_wrapper()
