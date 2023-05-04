from _rg.classes.PotentialContent import PotentialContent
from _rg.classes.RenderSettings import RenderSettings
from _rg.general import import_all_classes


class TestPotentialContent:
    def test_dump_all_schemas(self):
        PotentialContent.dump_all_schemas()

    def test_render(self):
        import_all_classes()
        for subclass in PotentialContent.__subclasses__():
            print(f"--- {subclass.__name__} ---")
            subclass().generate_pdf(RenderSettings())
