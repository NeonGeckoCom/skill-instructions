import json
import uuid

from json_parsing import JsonParser
from sound import Audio


class InstructionRunner:

    def __init__(self, lang):
        self.lang = lang or 'en'
        self.json_path = r'/home/mariia/neon-skill-instructions/instructions/en/demo1_en.jsonl'
        self.JsonParser = JsonParser(self.json_path, self.lang)
        self.json_list = self.JsonParser.json_reading()
        self.answer_list = []
        self.question_id = '1'
        self.Audio = Audio(self.lang)
        self.words_from_prev_answer = ''


    def execute(self):
        while int(self.question_id) != 0:
            if (len(self.answer_list) >= 3) and (self.answer_list[-3][0] == self.question_id) and (self.question_id != None):
                self.Audio.no_instructions()
                break
            else:
                result = self.JsonParser.conversation(self.json_list, self.question_id, self.words_from_prev_answer, self.answer_list)
                self.question_id = result[0]
                self.words_from_prev_answer = result[1]
                self.answer_list.append([self.question_id, self.words_from_prev_answer])
        else:
            self.Audio.finish()





    # def handle_incoming_instructions(self, **kwargs):
    #     {
    #         'index': 1,
    #         'question': 'How old are you?'
    #     }
    #
    #     instructions = {}
    #     instructions = json.loads(instructions)
    #     instructions_handler = JsonParser(instructions)
    #     new_handler_id = uuid.uuid4().hex
    #     self.instruction_handlers[new_handler_id] = instructions_handler
    #
    # def handle_interaction_with_instruction(self, **kwargs):
    #     data = {
    #         'question_num': 0,
    #         'response': 'Idk',
    #         'handler_id': '123'
    #     }
    #     return self.instruction_handlers.get(data['handler_id']).execute()