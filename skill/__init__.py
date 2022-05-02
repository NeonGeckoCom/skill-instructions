from neon_utils.skills.neon_skill import NeonSkill, LOG
from engine import InstructionRunner

class InstructionsSkill(NeonSkill):
    def __init__(self):
        super(InstructionsSkill, self).__init__(name="InstructionsSkill")

    # def initialize(self):
    #     self.register_intent_file("run_instructions.intent", self.handle_instructions)

    # @intent_handler(IntentBuilder("StartInstructions").require("start").require("instructions"))
    def handle_instructions(self, message):
        # TODO: Get instructions by name from message
        json_path = r'/home/mariia/neon-skill-instructions/instructions/en/demo2_en.jsonl'
        runner = InstructionRunner(json_path, 'en')
        runner.execute()
        #self.get_response()
        # TODO: in JsonParsing, `get_stt` can be replaced by self.get_response() which accepts a string to speak before waiting for a user response
        #       For speech that doesn't expect a user response, `self.speak()` should be used


def create_skill():
     return InstructionsSkill()

run_instructions = InstructionsSkill()
run_instructions.handle_instructions()