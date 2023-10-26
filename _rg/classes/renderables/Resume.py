from _rg.classes.RenderSettings import RenderSettings, RenderFormat
from _rg.classes.renderables.Header import Header
from _rg.classes.renderables.Renderable import Renderable
from _rg.classes.renderables.potential_content.BodyOfWork import BodyOfWork
from _rg.classes.renderables.potential_content.History import History
from _rg.classes.renderables.potential_content.SkillSet import SkillSet


class Resume(Renderable):
    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        if RenderSettings.render_format == RenderFormat.INDEED_HTML:
            return [
                Header(),
                History.summon(),
                SkillSet.summon(),
            ]

        return [
            Header(),
            SkillSet.summon(),
            BodyOfWork.summon(),
            History.summon(),
        ]
