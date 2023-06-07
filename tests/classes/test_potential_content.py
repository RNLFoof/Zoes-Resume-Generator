from pytest import assume

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.potential_content.PotentialContent import PotentialContent
from _rg.general import import_all_classes


class TestPotentialContent:
    def test_dump_all_schemas(self):
        PotentialContent.dump_all_schemas()

    # This is on potential content and not on renderable because rendes can't be summoned
    def test_render(self):
        import_all_classes()
        for subclass in PotentialContent.__subclasses__():
            print(f"--- {subclass.__name__} ---")
            with assume: subclass.summon().generate_pdf(r"S:\Code\Resume\tests\classes\out", RenderSettings())
