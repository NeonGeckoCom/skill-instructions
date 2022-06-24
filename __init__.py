from neon_utils.skills.neon_skill import NeonSkill, LOG
import os
import json
from mycroft.skills.core import intent_file_handler
from neon_utils.instruction_checks import Check


class InstructionsSkill(NeonSkill):

    def __init__(self):

        super(InstructionsSkill, self).__init__(name="InstructionsSkill")
        # json_path = basepath+'/scripts/en-us/demo2_en.jsonl'
        self.script_path = os.path.join(os.path.dirname(__file__), 'scripts')
        self.Check = None
        # self.json_path = None
        self.answer_list = []
        self.question_id = '1'
        self.words_from_prev_answer = ''

    def initialize(self):
        # When first run or prompt not dismissed, wait for load and prompt user
        if self.settings['prompt_on_start'] and not self.server:
            self.bus.once('mycroft.ready', self._start_instructions_prompt)

    @intent_file_handler("run_instructions.intent")
    def start_instructions_intent(self, message):
        LOG.info(message.data)

        self._start_instructions_prompt(message)
        return

    def json_reading(self, json_path):
      with open(json_path, 'r') as json_file:
          json_list = list(json_file)
          return json_list

    def finish(self):
        self.speak_dialog("finished")
        self.question_id = '1'

    def no_instruction(self):
        self.speak_dialog("no_instruction")
        self.question_id = '1'

    def repeat(self):
        self.speak_dialog("repeat")
    
    def instruction_selection(self, message):
        selected_instruction = []
        check = 1
        self.Check = Check(0, '', '', '')
        request_lang = message.data['lang'].split('-')[0]
        LOG.info(f"Checking lang... {os.listdir(self.script_path)}")
        if request_lang in os.listdir(self.script_path):
            folder_name = os.path.join(self.script_path, request_lang)
            while check != 0:
                self.speak_dialog("choose")
                instruction_name = self.get_response("instruction_names")
                numbers = [word for word in instruction_name if word.isdigit()]
                numbers = ''.join(numbers)
                if len(numbers)==0:
                    numbers = self.Check.is_number(str(instruction_name))
                    numbers = numbers[1]
                LOG.info(f"Instructions number ... {numbers}")
                selected_instruction = [name for name in os.listdir(folder_name) if str(numbers) in name]
                LOG.info(f"Selected path ... {str(selected_instruction)}")
                if len(selected_instruction) != 0:
                    self.speak_dialog("file_exists")
                    check = 0
                else:
                    self.speak_dialog("no_file")
            try:
                json_path = os.path.join(folder_name,
                                            selected_instruction[0])
                LOG.info('Your path: ' + json_path)
                self.handle_instructions(message, json_path)
                return
            except OSError as e:
                    self.speak('No such file: ' + str(e))
        else:
            LOG.info(f'{message.data["lang"]} is not supported yet.')
            self.speak('This lang is not supported yet.')
            return 

    def conversation(self, json_list, question_id, prev_answer, answer_list):
        for json_str in json_list:
            result = json.loads(json_str)
            if result['qa_id'] == question_id:
                # creating class veriable for using check functions
                self.Check = Check(question_id, prev_answer, result['question'], json_list)

                # listening to user's answer
                # recognizing words from wav file
                if result['answerable'] == "True":
                    # inserting user's previous answer into the question
                    if 'REPLACE' in result['question']:
                        text = self.Check.replace_question()
                        answer_words = self.get_response(text)
                    else:
                        answer_words = self.get_response(result['question'])
                    # checking for script in the answer variants
                    if 'answer_num_range' in result['answer'].keys():
                        return self.Check.answer_num_range(answer_words)
                    elif 'is_even_number' in result['answer'].keys():
                        return self.Check.is_even_number(answer_words)
                    elif 'is_number' in result['answer'].keys():
                        return self.Check.is_number(answer_words)
                    elif 'not_empty' in result['answer'].keys():
                        return self.Check.not_empty(answer_words)
                    elif 'check_answer' in result['answer'].keys():
                        return self.Check.check_answer(answer_words, answer_list)

                    # checking for existence of words in user's answer in correct answer
                    else:
                        if answer_words != None:
                            answer_words = answer_words.split(' ')
                            exist = [word for word in answer_words if word in result['answer'].keys()]
                            # return question id from json file
                            if len(exist) != 0:
                                question_id = result['answer'][exist[0]]
                                return str(question_id), ' '.join(answer_words)
                            # ask to repeat the question and return current question id
                            else:
                                self.repeat()
                                return str(question_id), ' '.join(answer_words)
                        else:
                            return str(0), self.repeat()
                else:
                    if 'REPLACE' in result['question']:
                        # inserting user's previous answer into the question
                        text = self.Check.replace_question()
                        self.speak(text)
                        return str(question_id+1), prev_answer
                    else:
                        self.speak(result['question'])
                        return str(question_id+1), prev_answer
    
    def execute(self, json_list):
        while int(self.question_id) != 0:
            if (len(self.answer_list) >= 3) and (self.answer_list[-3][0] == self.question_id) and (self.question_id != None):
                self.no_instruction()
                break
            else:
                result = self.conversation(json_list, self.question_id,
                                           self.words_from_prev_answer,
                                           self.answer_list)
                LOG.info(result)
                self.question_id = result[0]
                self.words_from_prev_answer = result[1]
                self.answer_list.append([self.question_id, self.words_from_prev_answer])
        else:
            self.finish()

    def _start_instructions_prompt(self, message):
        LOG.info('Prompting Instructions start')
        self.make_active()
        start_instr = self.ask_yesno("start")
        if start_instr == "yes":
            # selection of the istruction according to user's answer
            self.instruction_selection(message)
            return
        else:
            repeat_instr = self.ask_yesno("Do you want to stop instructions?")
            if repeat_instr == 'yes':
                self.speak('Okey, goodbye!')
            else:
                self.instruction_selection(message)
                return

    def handle_instructions(self, message, json_path):
        # TODO: Get instructions by name from message
        if self.neon_in_request(message):
            json_list = self.json_reading(json_path)
            self.execute(json_list)
                

def create_skill():
    return InstructionsSkill()
