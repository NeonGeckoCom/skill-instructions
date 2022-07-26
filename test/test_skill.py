# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import shutil
import unittest
import pytest

from os import mkdir
from os.path import dirname, join, exists
from mock import Mock
from ovos_utils.messagebus import FakeBus

from mycroft.skills.skill_loader import SkillLoader

from mycroft_bus_client import Message


class TestSkill(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        bus = FakeBus()
        bus.run_in_thread()
        skill_loader = SkillLoader(bus, dirname(dirname(__file__)))
        skill_loader.load()
        cls.skill = skill_loader.instance

        # Define a directory to use for testing
        cls.test_fs = join(dirname(__file__), "skill")
        if not exists(cls.test_fs):
            mkdir(cls.test_fs)

        # Override the configuration and fs paths to use the test directory
        cls.skill.settings_write_path = cls.test_fs
        cls.skill.file_system.path = cls.test_fs
        cls.skill._init_settings()
        cls.skill.initialize()

        # Override speak and speak_dialog to test passed arguments
        cls.skill.speak = Mock()
        cls.skill.speak_dialog = Mock()

        # TODO: Put any skill method overrides here

    def setUp(self):
        self.skill.speak.reset_mock()
        self.skill.speak_dialog.reset_mock()

        # TODO: Put any cleanup here that runs before each test case

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.test_fs)

    def test_en_skill_init(self):
        real_askyesno = self.skill.ask_yesno
        real_execute = self.skill.execute
        real_instruction_selection = self.skill.instruction_selection
        self.skill.ask_yesno = Mock(return_value="yes")
        self.skill.execute = Mock()
        self.skill.instruction_selection = Mock()
        test_file_path = join(dirname(dirname(__file__)), "instructions", "en",
                              "demo1_en-us.jsonl")
        self.skill.handle_instructions(
            Message('test', {'utterance': 'start instructions', 'lang': 'en-us'},
                    {'context_key': 'Instructions'}), test_file_path)
        self.skill.execute.assert_called_once()

        message = Message('test', {'utterance': 'start instructions',
                                   'lang': 'en-us'},
                          {'context_key': 'Instructions'})
        self.skill._start_instructions_prompt(message)
        self.skill.ask_yesno.assert_called_once_with("start")
        self.skill.instruction_selection.assert_called_once_with(message)

        self.skill.execute = real_execute
        self.skill.ask_yesno = real_askyesno
        self.skill.instruction_selection = real_instruction_selection

    def test_uk_skill_init(self):
        real_askyesno = self.skill.ask_yesno
        real_execute = self.skill.execute
        real_instruction_selection = self.skill.instruction_selection
        self.skill.ask_yesno = Mock(return_value="yes")
        self.skill.execute = Mock()
        self.skill.instruction_selection = Mock()
        test_file_path = join(dirname(dirname(__file__)), "instructions", "uk",
                              "demo1_uk.jsonl")
        self.skill.handle_instructions(
            Message('test', {'utterance': 'запустити інструкції', 'lang': 'uk-ua'},
                    {'context_key': 'інструкції'}), test_file_path)
        message = Message('test', {'utterance': 'запустити інструкції',
                                   'lang': 'uk-ua'},
                          {'context_key': 'інструкції'})
        self.skill._start_instructions_prompt(message)

        self.skill.ask_yesno.assert_called_once_with("start")
        self.skill.instruction_selection.assert_called_once_with(message)

        self.skill.execute = real_execute
        self.skill.ask_yesno = real_askyesno
        self.skill.instruction_selection = real_instruction_selection


if __name__ == '__main__':
    pytest.main()
