from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.Header import Header
from _rg.classes.renderables.Renderable import Renderable
from _rg.classes.renderables.potential_content.Accomplishment import AccomplishmentSet
from _rg.classes.renderables.potential_content.History import History
from _rg.classes.renderables.potential_content.SkillSet import SkillSet


class Resume(Renderable):
    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        return [
            Header(),
            SkillSet.summon(),
            AccomplishmentSet.summon(),
            History.summon(),
        ]
