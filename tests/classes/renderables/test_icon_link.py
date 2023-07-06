import pytest
from pytest_assume.plugin import assume

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.IconLink import IconLink
from _rg.classes.renderables.WithEmphasis import WithEmphasis


class TestIconLink:
    def test_icon_name(self):
        with assume: assert IconLink("https://en.wikipedia.org/wiki/Main_Page").icon_name() == "wikipedia"
        with assume: assert IconLink("https://www.linkedin.com/in/zoe-zablotsky-598b2018a/").icon_name() == "linkedin"
        with assume: assert IconLink("https://github.com/RNLFoof").icon_name() == "github"
        with pytest.raises(Exception): IconLink("burp").icon_name()

    def test_render(self):
        with assume:
            WithEmphasis(1, [
                IconLink("https://github.com/RNLFoof")
            ]).generate_pdf(r"S:\Code\Resume\tests\classes\out", RenderSettings())
