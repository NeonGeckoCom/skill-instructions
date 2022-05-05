from neon_utils.skills.neon_skill import NeonSkill, LOG
from engine import InstructionRunner
from mycroft_bus_client import Message
import os

class InstructionsSkill(NeonSkill):
    def __init__(self):
        super(InstructionsSkill, self).__init__(name="InstructionsSkill")

    def initialize(self):
        self.register_intent_file("run_instructions.intent", self.handle_instructions)

        # When first run or demo prompt not dismissed, wait for load and prompt user
        if self.settings['prompt_on_start'] and not self.server:
            self.bus.once('mycroft.ready', self._start_instructions_prompt)

    # @intent_handler(IntentBuilder("StartInstructions").require("start").require("instructions"))

    def _start_instructions_prompt(self, message):
        LOG.debug('Prompting Instructions start')
        self.make_active()
        start_instr = self.ask_yesno()
        if start_instr == 'yes':
            self.handle_instructions(message)
            return

    def handle_instructions(self, message):
        # TODO: Get instructions by name from message
        basepath = os.path.dirname(os.path.realpath(__file__))
        json_path = basepath+'/instructions/en/demo2_en.jsonl'
        if self.neon_in_request(message):
            if self.request_from_mobile(message):
                pass
            elif self.server:
                pass
            else:
                runner = InstructionRunner(json_path)
                runner.execute()
        # TODO: in JsonParsing, `get_stt` can be replaced by self.get_response() which accepts a string to speak before waiting for a user response
        #       For speech that doesn't expect a user response, `self.speak()` should be used


def create_skill():
     return InstructionsSkill()

run_instructions = InstructionsSkill()
run_instructions.handle_instructions(Message("mycroft.ready"))