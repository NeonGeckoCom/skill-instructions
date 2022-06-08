from neon_utils.skills.neon_skill import NeonSkill, LOG
import os
import json
from mycroft.skills.core import intent_file_handler
from neon_utils.instruction_checks import Check

class InstructionsSkill(NeonSkill):

    def __init__(self):

        super(InstructionsSkill, self).__init__(name="InstructionsSkill")
        basepath = os.path.dirname(os.path.realpath(__file__))
        json_path = basepath+'/scripts/en-us/demo2_en.jsonl'
        self.script_path = basepath+'/scripts'
        self.json_path = json_path
        self.Check = None
        self.json_path = json_path
        self.answer_list = []
        self.question_id = '1'
        self.words_from_prev_answer = ''


    @intent_file_handler("run_instructions.intent")
    def start_instructions_intent(self, message):
        LOG.info(message.data)
        #When first run or prompt not dismissed, wait for load and prompt user
        if self.settings['prompt_on_start'] and not self.server:
            self.bus.once('mycroft.ready', self._start_instructions_prompt(message))
        self._start_instructions_prompt(message)
        return


    def json_reading(self):
      with open(self.json_path, 'r') as json_file:
          json_list = list(json_file)
          return json_list

    def finish(self):
        if self.lang == 'uk':
            self.speak('Закінчили.')
        elif self.lang == 'pl':
            self.speak('Skończone.')
        else:
            self.speak('Finished.')
        self.question_id = '1'

    def no_instruction(self):
        if self.lang == 'uk':
            self.speak('Немає інструкцій для цього випадку.')
        elif self.lang == 'pl':
            self.speak('Brak struktury dla tej sprawy.')
        else:
            self.speak('No instructions for this case.')
        self.question_id = '1'

    def repeat(self):
        if self.lang == 'uk':
            self.speak('Повторіть, будь-ласка.')
        elif self.lang == 'pl':
            self.speak('Powtórz proszę.')
        else:
            self.speak('Repeat, please.')
    
    def instruction_selection(self, message):
        selected_instruction = ''
        for folder in os.walk(self.script_path):
            if message.data['lang'] in folder[1]:
                folder_name = folder[0]+'/'+message.data['lang']+'/'
                for script in os.walk(folder_name):
                    if message.data['lang'] == 'uk':
                        instruction_name = self.get_response('Виберіть із наявних інструкцій: '+" ".join(script[2]))
                    elif message.data['lang'] == 'pl':
                        instruction_name = self.get_response('Wybierz z istniejących instrukcji: '+" ".join(script[2]))
                    else:
                        instruction_name = self.get_response('Select from existing instructions: '+" ".join(script[2]))
                    selected_instruction = [name for name in script[2] if instruction_name in name]
                    try:
                        self.json_path = folder_name+selected_instruction[0]
                        self.speak('Your path: ' + self.json_path)
                        self.handle_instructions(message)
                    except OSError as e:
                        self.speak('No such file: '+ str(e))
                        self.json_path = folder_name+''
                        self.speak('starting: '+self.json_path)
                        self.handle_instructions(message)
            else:
                LOG.info('This lang is not supported yet.')
                self.speak('This lang is not supported yet.')


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
    
    def execute(self):
        while int(self.question_id) != 0:
            if (len(self.answer_list) >= 3) and (self.answer_list[-3][0] == self.question_id) and (self.question_id != None):
                self.no_instruction()
                break
            else:
                result = self.conversation(self.json_list, self.question_id, self.words_from_prev_answer, self.answer_list)
                self.question_id = result[0]
                self.words_from_prev_answer = result[1]
                self.answer_list.append([self.question_id, self.words_from_prev_answer])
        else:
            self.finish()


    def _start_instructions_prompt(self, message):
        LOG.info('Prompting Instructions start')
        self.make_active()
        start_instr = self.ask_yesno("Would you like me to start the instructions?")
        if start_instr == 'yes':
            # selection of ithe nstruction according to user's answer
            self.instruction_selection(message)
            return
    

    def handle_instructions(self, message):
        # TODO: Get instructions by name from message
        if self.neon_in_request(message):
            self.json_list = self.json_reading()
            self.execute()
                

def create_skill():
     return InstructionsSkill()
