import importlib
import os
import re

import json5
from pydantic import BaseModel


class PotentialContent(BaseModel):
    _singletons: dict[str, "PotentialContent"] = {}

    def __init__(self, data_override=None):
        with open(self.SAVED_TO, "rb") as f:
            if data_override is not None:
                super().__init__(**data_override)
            else:
                super().__init__(**json5.load(f))
        if self.__class__.__name__ in PotentialContent._singletons:
            raise Exception(f"Already initialized! Use {self.__class__.__name__}.summon.")

    @classmethod
    def summon(cls):
        if cls.__name__ not in PotentialContent._singletons:
            PotentialContent._singletons[cls.__name__] = cls()  # Not done with setdefault so that it doesn't evaluate
        return PotentialContent._singletons[cls.__name__]

    @classmethod
    def dump_all_schemas(cls):
        # All classes need to be loaded, because otherwise Python doesn't know what subclasses exist
        class_path = os.path.join(
            os.path.split(__file__)[0],
            "../../_rg/classes")
        for class_filename in os.listdir(class_path):
            class_name, _ = os.path.splitext(class_filename)
            importlib.import_module("_rg.classes." + class_name)

        # Actually dump
        for subclass in cls.__subclasses__():
            subclass._dump_schema()

    @classmethod
    def camelcase_name(cls):
        return re.sub(r"[a-z][A-Z]", lambda match: "{0[0]}_{0[1]}".format(match.group(0)), cls.__name__).lower()

    @classmethod
    @property
    def SAVED_TO(cls) -> str:
        return os.path.join(
            os.path.abspath(os.path.split(__file__)[0]),
            f"../potential_content/{cls.camelcase_name()}.json5"
        )

    @classmethod
    @property
    def SCHEMA_SAVED_TO(cls) -> str:
        return os.path.join(
            os.path.abspath(os.path.split(__file__)[0]),
            f"../schema/{cls.camelcase_name()}.json"
        )

    @classmethod
    def _dump_schema(cls) -> None:
        """Updates the schema used to validate the skill set provided in data/skillSet.json5."""
        with open(cls.SCHEMA_SAVED_TO, "w") as f:
            f.write(cls.schema_json(indent=4))
