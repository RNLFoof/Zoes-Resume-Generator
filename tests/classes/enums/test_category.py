from pytest import assume

from _rg.classes.enums.Category import Category


class TestCategory:
    def test_init(self):
        with assume: assert Category.PROGRAMMING.name == "PROGRAMMING"
        with assume: assert len({c.number for c in Category}) == len(Category)
        with assume: assert Category.PROGRAMMING._default_usage == "That's what it's written in"
        with assume: assert Category.THREED_MODELING._display_name == "3D Modeling and Printing"
        with assume: assert Category.SHAREPOINT._subcategory_of == Category.OFFICE_SOFTWARE.value

    def test_display_name(self):
        with assume: assert Category.PROGRAMMING.display_name == "Programming"
        with assume: assert Category.THREED_MODELING.display_name == "3D Modeling and Printing"

    def test_subcategory_of(self):
        with assume: assert Category.SHAREPOINT.subcategory_of == Category.OFFICE_SOFTWARE

    def test_default_usage(self):
        with assume: assert type(Category.PROGRAMMING.default_usage) is str
        with assume: assert type(Category.PROGRAMMING._default_usage) is str
        with assume: assert Category.PROGRAMMING.default_usage == "That's what it's written in"
