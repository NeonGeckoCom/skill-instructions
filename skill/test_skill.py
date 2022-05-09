import os
import shutil
import unittest
from os import mkdir

import pytest

from time import sleep
from copy import deepcopy
from os.path import dirname, join, exists
from mock import Mock
from mycroft_bus_client import Message
from ovos_utils.messagebus import FakeBus

print(dirname(dirname(__file__)))

class TestSkill(unittest.TestCase):

    # run_instructions = InstructionsSkill()
    # run_instructions.handle_instructions(Message("mycroft.ready"))

    @classmethod
    def setUpClass(cls) -> None:
        from mycroft.skills.skill_loader import SkillLoader

        bus = FakeBus()
        bus.run_in_thread()
        skill_loader = SkillLoader(bus, dirname(dirname(__file__)))
        skill_loader.load()
        cls.skill = skill_loader.instance
        cls.test_fs = join(dirname(__file__), "skill_fs")
        if not exists(cls.test_fs):
            mkdir(cls.test_fs)
        cls.skill.initialize()
        # Override speak and speak_dialog to test passed arguments
        cls.skill.speak = Mock()
        cls.skill.speak_dialog = Mock()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.test_fs)

    def test_00_skill_init(self):
        # Test any parameters expected to be set in init or initialize methods
        from neon_utils.skills import NeonSkill




if __name__ == '__main__':
    pytest.main()