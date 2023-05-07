import json
import os.path
from inspect import getsource
from pathlib import Path
from typing import Callable

import pytest
from _pytest.monkeypatch import MonkeyPatch

from _rg.classes.enums.Category import Category
from _rg.classes.enums.Impressiveness import Impressiveness
from _rg.classes.renderables.potential_content.PotentialContent import PotentialContent
from _rg.classes.renderables.potential_content.SkillSet import Skill, SkillSet


@pytest.fixture
def common_competence() -> int:
    return 2


@pytest.fixture
def common_impressiveness() -> Impressiveness:
    for y in filter(lambda x: x.number == 3, list(Impressiveness)):
        return y


@pytest.fixture
def common_category() -> Category:
    for y in filter(lambda x: x.name == "PROGRAMMING", list(Category)):
        return y


@pytest.fixture
def common_skill(common_competence: int, common_impressiveness: Impressiveness, common_category: Category) -> Skill:
    return Skill(competence=common_competence, impressiveness=common_impressiveness, category=common_category)


@pytest.fixture
def common_skill_set_dict() -> dict:
    return {
        "skills": {
            "Bad Skill": {
                "impressiveness": Impressiveness.NONE.name,
                "competence": 1,
                "category": "PROGRAMMING"
            },
            "Mediocre Skill": {
                "impressiveness": Impressiveness.BEGINNER.name,
                "competence": 3,
                "category": "PROGRAMMING"
            },
            "Good Skill": {
                "impressiveness": Impressiveness.SPECIALIZABLE.name,
                "competence": 5,
                "category": "PROGRAMMING"
            },
        }
    }


@pytest.fixture
def common_skill_set(common_skill_set_dict) -> SkillSet:
    PotentialContent._singletons.pop(SkillSet.__name__, None)
    return SkillSet(data_override=common_skill_set_dict)


class TestSkill:
    def test_init(self, common_competence: int, common_impressiveness: Impressiveness, common_skill: Skill):
        assert (
                   common_competence,
                   common_impressiveness,
               ) == (
                   common_skill.competence,
                   common_skill.impressiveness,
               )

    def test_generic_value_a(self, common_skill: Skill):
        assert common_skill.generic_value() == 6

    @staticmethod
    @pytest.mark.parametrize("skill_name, expected_value",
                             [("Bad Skill", 0), ("Mediocre Skill", 6), ("Good Skill", 25)])
    def test_generic_value_b(skill_name: str, expected_value: int, common_skill_set: SkillSet):
        skill = common_skill_set.skills[skill_name]
        assert skill.generic_value() == expected_value


class TestSkillSet:
    @staticmethod
    def test_dump_schema(monkeypatch: MonkeyPatch, tmp_path: Path):
        temp_schema_saved_to = tmp_path / "skillSetSchema.json"
        monkeypatch.setattr(SkillSet, "SCHEMA_SAVED_TO", temp_schema_saved_to)
        SkillSet._dump_schema()
        assert os.path.exists(temp_schema_saved_to)

    @staticmethod
    @pytest.mark.parametrize("check, expected_value", [
        (lambda context: context["skill_set_all"], lambda context: context["common_skill_set"]),
        (lambda context: context["skill_set_all"].skills["Bad Skill"].name, lambda context: "Bad Skill"),
    ])
    def test_init(common_skill_set_dict: dict, common_skill_set: SkillSet, monkeypatch: MonkeyPatch,
                  tmp_path: Path, check: Callable, expected_value):
        temp_saved_to = tmp_path / "skillSetSaved.json"
        monkeypatch.setattr(SkillSet, "SAVED_TO", temp_saved_to)
        with open(temp_saved_to, "w") as f:
            json.dump(common_skill_set_dict, f)
        context = {
            "skill_set_all": SkillSet.summon(),
            "common_skill_set": common_skill_set
        }
        assert check(context) == expected_value(context), f"This behavior failed: {getsource(check).strip()}"

    @staticmethod
    @pytest.mark.parametrize("key, expected_order", [
        (lambda skill: skill.competence, [1, 3, 5]),
        (lambda skill: -skill.competence, [5, 3, 1]),
        (lambda skill: skill.impressiveness.number, [1, 3, 5]),
        (lambda skill: skill.impressiveness, [1, 3, 5]),
        (lambda skill: skill.generic_value(), [1, 3, 5]),
    ])
    def test_skills_by(common_skill_set: SkillSet, key, expected_order):
        assert [skill.competence for skill in common_skill_set._skills_by(key)] == expected_order, \
            f"This behavior failed: {getsource(key).strip()}"

    @staticmethod
    def test_skills_by_generic_value(common_skill_set: SkillSet):
        assert [skill.competence for skill in common_skill_set.skills_by_generic_value()] == [5, 3, 1]
