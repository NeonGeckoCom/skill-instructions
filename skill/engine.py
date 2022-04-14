import json
import uuid

from skill.json_parsing import JsonParser


class InstructionRunner:

    def __init__(self):
        self.instruction_handlers = {}

    def handle_incoming_instructions(self, **kwargs):
        {
            'index': 1,
            'question': 'How old are you?'
        }

        instructions = {}
        instructions = json.loads(instructions)
        instructions_handler = JsonParser(instructions)
        new_handler_id = uuid.uuid4().hex
        self.instruction_handlers[new_handler_id] = instructions_handler

    def handle_interaction_with_instruction(self, **kwargs):
        data = {
            'question_num': 0,
            'response': 'Idk',
            'handler_id': '123'
        }
        return self.instruction_handlers.get(data['handler_id']).execute()