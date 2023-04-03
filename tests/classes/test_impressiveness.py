from _rg.classes.Impressiveness import Impressiveness


class TestImpressiveness:
    def test_init_number(self):
        number = 5
        impressiveness = Impressiveness.NONE
        impressiveness.__init__(number, "")
        assert impressiveness.number == number

    def test_init_description(self):
        description = "Hey"
        impressiveness = Impressiveness.NONE
        impressiveness.__init__(0, description)
        assert impressiveness.description == description

    def test_modify_schema_desc(self):
        schema = {}
        Impressiveness.__modify_schema__(schema)
        assert schema["description"].count("\n") == 0

    def test_modify_schema_enum_is_strs(self):
        schema = {}
        Impressiveness.__modify_schema__(schema)
        assert all(type(name) is str for name in schema["enum"])

    def test_modify_schema_enum_is_uppercase(self):
        schema = {}
        Impressiveness.__modify_schema__(schema)
        assert all(str(name).isupper() for name in schema["enum"])

    def test_get_validators(self):
        assert [x for x in Impressiveness.__get_validators__()][0]("NONE") == Impressiveness.NONE

    def test_lower_bound(self):
        assert Impressiveness.lower_bound() == 0

    def test_upper_bound(self):
        assert Impressiveness.upper_bound() == 5
