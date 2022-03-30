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
import re
import os
from sound import Audio


class JsonParsing:
    def __init__(self, json_path):
        self.json_path = json_path
        self.json_list = None
        self._ANSWERS = [] #all user's answers during the session


    def json_reading(self):
      with open(self.json_path, 'r') as json_file:
          json_list = list(json_file)
          self.json_list = json_list

    def execute(self):
        answer_list = []
        answer = 1
        prev_words = ' '
        while int(answer) != 0:
            if (len(answer_list) >= 3) and (answer_list[-3] == answer) and (answer != None):
                if self.lang == 'en':
                    call_tts('No instructure for this case.', '0')
                elif self.lang == 'pl':
                    call_tts('Brak struktury dla tej sprawy.', '0')
                break
            else:
                result = conversation(self.json_list, answer, prev_words)
                answer = result[0]
                prev_words = result[1]
                remember(answer - 1, prev_words)
                answer_list.append(answer)
                print(ANSWERS)
        else:
            if self.lang == 'en':
                call_tts('Finished', '0')
            elif self.lang == 'pl':
                call_tts('Skończone', '0')

ANSWERS = []
path = '/content/drive/MyDrive/Polish_STT/demo2_pl.jsonl'
parser = JsonParsing(path, 'en')
