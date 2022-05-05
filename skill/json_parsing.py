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

import json
from threading import Event

# from sound import Audio
from answer_checks import Check
from neon_utils.skills.neon_skill import NeonSkill


class JsonParser():
    def __init__(self, json_path: str):
        '''
        lang: ISO 639-1
        '''
        # self.Audio = Audio(bus, lang)
        self.json_path = json_path
        self.Check = None

    def json_reading(self):
      with open(self.json_path, 'r') as json_file:
          json_list = list(json_file)
          return json_list


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
                        answer_words = NeonSkill.get_response(text)
                    else:
                        print('here')
                        answer_words = NeonSkill.get_response(result['question'])
                
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
                        answer_words = answer_words.split(' ')
                        exist = [word for word in answer_words if word in result['answer'].keys()]
                        # return question id from json file
                        if len(exist) != 0:
                            question_id = result['answer'][exist[0]]
                            return str(question_id), ' '.join(answer_words)
                        # ask to repeat the question and return current question id
                        else:
                            NeonSkill.speak('Repeat, please')
                            return str(question_id), ' '.join(answer_words)
                else:
                    if 'REPLACE' in result['question']:
                    # inserting user's previous answer into the question
                        text = self.Check.replace_question()
                        NeonSkill.speak(text)
                        return str(question_id+1), prev_answer
                    else:
                        NeonSkill.speak(result['question'])
                        return str(question_id+1), prev_answer


