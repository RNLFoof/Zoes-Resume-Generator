from _rg.classes.RenderSettings import RenderSettings


class Renderable:
    def render(self, render_settings: RenderSettings) -> str:
        raise NotImplementedError()
