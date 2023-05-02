from _rg.classes.RenderSettings import RenderSettings


class Renderable:
    def render(self, render_settings: RenderSettings) -> list[str]:
        raise NotImplementedError()

    def render_as_string(self, render_settings: RenderSettings) -> str:
        return "".join(self.render(render_settings))
