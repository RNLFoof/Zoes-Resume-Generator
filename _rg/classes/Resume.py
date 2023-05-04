from _rg.classes.Accomplishment import AccomplishmentSet
from _rg.classes.Header import Header
from _rg.classes.History import History
from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.Renderable import Renderable, RecursiveStrList
from _rg.classes.SkillSet import SkillSet


class Resume(Renderable):
    def render(self, render_settings: RenderSettings) -> RecursiveStrList:
        return [
            Header(),
            SkillSet.summon().render(render_settings),
            AccomplishmentSet.summon().render(render_settings),
            History.summon().render(render_settings),
        ]
