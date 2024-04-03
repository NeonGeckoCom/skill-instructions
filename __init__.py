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


import os
import json
from neon_utils.skills.neon_skill import NeonSkill
from ovos_utils import classproperty
from ovos_utils.log import LOG
from ovos_utils.process_utils import RuntimeRequirements
from ovos_workshop.decorators import intent_handler
from skill_instructions.instruction_checks import Check


class InstructionsSkill(NeonSkill):
    def __init__(self, **kwargs):
        NeonSkill.__init__(self, **kwargs)
        self.script_path = os.path.join(os.path.dirname(__file__),
                                        'instructions')
        self.Check = None
        self.answer_list = []
        self.question_id = '1'
        self.words_from_prev_answer = ''

    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(network_before_load=False,
                                   internet_before_load=False,
                                   gui_before_load=False,
                                   requires_internet=False,
                                   requires_network=False,
                                   requires_gui=False,
                                   no_internet_fallback=True,
                                   no_network_fallback=True,
                                   no_gui_fallback=True)

    def initialize(self):
        # When first run or prompt not dismissed, wait for load and prompt user
        if self.settings.get('prompt_on_start'):
            self.bus.once('mycroft.ready', self._start_instructions_prompt)

    @intent_handler("run_instructions.intent")
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

    def lang_check(self, message):
        LOG.info(f"Message is {message.data}")
        request_lang = message.data['lang'].split('-')[0]
        LOG.info(f"Checking lang... {os.listdir(self.script_path)}")
        if request_lang in os.listdir(self.script_path):
            return True, request_lang
        else:
            LOG.info(f'{message.data["lang"]} is not supported yet.')
            self.speak_dialog('finished')
            return  False, request_lang

    def open_instructions_file(self, folder_name, selected_instruction, message):
        try:
            json_path = os.path.join(folder_name,
                                        selected_instruction)
            LOG.info('Your path: ' + json_path)
            self.handle_instructions(message, json_path)
            return
        except OSError as e:
            LOG.info('File path is broken: ' + str(e))
            self.speak_dialog('finished')
    
    def instruction_selection(self, message):
        instruction_name = ''
        selected_instruction = []
        check = 1
        self.Check = Check(0, '', '', '')
        lang = self.lang_check(message)
        if lang[0]== True:
            folder_name = os.path.join(self.script_path, lang[1])
            while (self.voc_match(instruction_name, "no") != True):
                if check <= 3:
                    LOG.info(f"Check is ... {check}")
                    self.speak_dialog("choose")
                    instruction_name = self.get_response("instruction_names")
                    if instruction_name != None:
                        LOG.info('No voc is matched: ' + str(self.voc_match(instruction_name, "no")))
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
                            self.open_instructions_file(folder_name, selected_instruction[0], message)
                        else:
                            self.speak_dialog("no_file")
                            check+=1
                    else:
                        self.speak_dialog('finished')
                        return
                else:
                    self.speak_dialog('finished')
                    return
            else:
                self.speak_dialog('finished')
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
                self.speak_dialog('finished')
            else:
                self.instruction_selection(message)
                return

    def handle_instructions(self, message, json_path):
        # TODO: Get instructions by name from message
        if self.neon_in_request(message):
            json_list = self.json_reading(json_path)
            self.execute(json_list)
