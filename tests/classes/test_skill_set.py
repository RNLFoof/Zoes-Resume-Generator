import json
from inspect import getsource
import os.path
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch

from _rg.classes.Impressiveness import Impressiveness
from _rg.classes.SkillSet import Skill, SkillSet


@pytest.fixture
def common_competence() -> int:
    return 2


@pytest.fixture
def first_impressiveness() -> Impressiveness:
    return list(Impressiveness)[0]


@pytest.fixture
def common_impressiveness(first_impressiveness: Impressiveness) -> Impressiveness:
    first_impressiveness.__init__(3, "")
    return first_impressiveness


@pytest.fixture
def common_skill(common_competence: int, common_impressiveness: Impressiveness) -> Skill:
    return Skill(competence=common_competence, impressiveness=common_impressiveness)


@pytest.fixture
def common_skill_set_dict() -> dict:
    return {
        "skills": {
            "Bad Skill": {
                "impressiveness": Impressiveness.NONE.name,
                "competence": 1
            },
            "Mediocre Skill": {
                "impressiveness": Impressiveness.BEGINNER.name,
                "competence": 3
            },
            "Good Skill": {
                "impressiveness": Impressiveness.SPECIALIZABLE.name,
                "competence": 5
            },
        }
    }


@pytest.fixture
def common_skill_set() -> SkillSet:
    return SkillSet(
        skills={
            "Bad Skill": Skill(
                impressiveness=Impressiveness.NONE,
                competence=1
            ),
            "Mediocre Skill": Skill(
                impressiveness=Impressiveness.BEGINNER,
                competence=3
            ),
            "Good Skill": Skill(
                impressiveness=Impressiveness.SPECIALIZABLE,
                competence=5
            ),
        }
    )


class TestSkill:
    def test_init(self, common_competence: int, common_impressiveness: Impressiveness, common_skill: Skill):
        assert (
                   common_competence,
                   common_impressiveness,
               ) == (
                   common_skill.competence,
                   common_skill.impressiveness,
               )

    def test_generic_value(self, common_skill: Skill):
        assert common_skill.generic_value() == 6


class TestSkillSet:
    @staticmethod
    def test_dump_schema(monkeypatch: MonkeyPatch, tmp_path: Path):
        temp_schema_saved_to = tmp_path / "skillSetSchema.json"
        monkeypatch.setattr(SkillSet, "SCHEMA_SAVED_TO", temp_schema_saved_to)
        SkillSet._dump_schema()
        assert os.path.exists(temp_schema_saved_to)

    @staticmethod
    def test_all(common_skill_set_dict: dict, common_skill_set: SkillSet, monkeypatch: MonkeyPatch,
                 tmp_path: Path):
        temp_saved_to = tmp_path / "skillSetSaved.json"
        monkeypatch.setattr(SkillSet, "SAVED_TO", temp_saved_to)
        with open(temp_saved_to, "w") as f:
            json.dump(common_skill_set_dict, f)
        assert SkillSet.all() == common_skill_set

    @staticmethod
    @pytest.mark.parametrize("key, expected_order", [
        (lambda name, skill: skill.competence, [1, 3, 5]),
        (lambda name, skill: -skill.competence, [5, 3, 1]),
        (lambda name, skill: skill.impressiveness.number, [1, 3, 5]),
        (lambda name, skill: skill.impressiveness, [1, 3, 5]),
        (lambda name, skill: skill.generic_value(), [1, 3, 5]),
    ])
    def test_skills_by(common_skill_set: SkillSet, key, expected_order):
        assert [skill.competence for name, skill in common_skill_set._skills_by(key)] == expected_order, \
            f"This behavior failed: {getsource(key).strip()}"

    @staticmethod
    def test_skills_by_generic_value(common_skill_set: SkillSet):
        assert [skill.competence for name, skill in common_skill_set.skills_by_generic_value()] == [5, 3, 1]
