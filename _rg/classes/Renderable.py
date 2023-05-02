from itertools import chain
from typing import TypeVar, Self, Generic

from _rg.classes.RenderSettings import RenderSettings

RecursiveStrList = TypeVar("RecursiveStrList", str, list[str], Self)


class Renderable:
    def render(self, render_settings: RenderSettings) -> Generic[RecursiveStrList]:
        raise NotImplementedError()

    def render_as_string(self, render_settings: RenderSettings) -> str:
        return "".join(
            chain.from_iterable(
                self.render(render_settings)
            )
        )
