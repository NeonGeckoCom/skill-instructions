import json
import uuid

from json_parsing import JsonParser
from neon_utils.skills.neon_skill import NeonSkill


class InstructionRunner(NeonSkill):

    def __init__(self, json_path: str, lang: str):
        self.lang = lang or 'en'
        self.json_path = json_path
        self.JsonParser = JsonParser(self.json_path, self.lang)
        self.json_list = self.JsonParser.json_reading()
        self.answer_list = []
        self.question_id = '1'
        # self.Audio = Audio(self.lang)
        self.words_from_prev_answer = ''


    def execute(self):

        while int(self.question_id) != 0:
            if (len(self.answer_list) >= 3) and (self.answer_list[-3][0] == self.question_id) and (self.question_id != None):
                print('no instructions')
                self.speak('no instructions')
                # self.Audio.no_instructions()
                break
            else:
                print(self.question_id)
                print(self.words_from_prev_answer)
                result = self.JsonParser.conversation(self.json_list, self.question_id, self.words_from_prev_answer, self.answer_list)
                print(result)
                self.question_id = result[0]
                self.words_from_prev_answer = result[1]
                self.answer_list.append( [self.question_id, self.words_from_prev_answer])
        else:
            print('finish')
            self.speak('Finished')
            #self.Audio.finish()

json_path = r'/home/mariia/neon-skill-instructions/instructions/en/demo1_en.jsonl'
runner = InstructionRunner(json_path, 'en')
runner.execute()