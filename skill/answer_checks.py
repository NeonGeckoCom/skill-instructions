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

from word2number import w2n
import re

class Check:
    def __init__(self, id, answer):
        self.id = id
        self.answer = answer

    def answer_range(self, id, answer):
      try:
          numbers = w2n.word_to_num(answer)
          print('numbers:', numbers)
          if numbers >= 1 and numbers <= 10:
            return id+1, numbers
      except ValueError:
          print('no numbers in the answer')
          return id, answer

    def even_number(self, id, answer):
      try:
          numbers = w2n.word_to_num(answer)
          if numbers >= 2 and (numbers % 2) == 0:
            return id+1, numbers
          else:
            return id, numbers
      except ValueError:
          print('no numbers in the answer')
          return id, answer

    def is_number(self, id, answer):
      try:
          numbers = w2n.word_to_num(answer)
          return id+1, numbers
      except ValueError:
          print('no numbers in the answer')
          return id, answer

    def not_empty(self, id, answer):
      if str(answer) != '':
            return id+1, answer
      else:
            return id, answer

    def replace_question(self, prev_answer, question):
        '''
        replaces the word REPLACE in the question
        with the word from previouse user's answer
        '''
        print(str(prev_answer))
        new_question = re.sub('REPLACE', str(prev_answer), str(question))
        return new_question

    def check_answer(self, ANSWERS, id, answer):
      try:
          numbers = w2n.word_to_num(answer)
          for answer in ANSWERS:
            if answer[0] == 2:
              answer_2 = answer[1]/2
          if numbers == answer_2:
            return id+1, numbers
          else:
            return id+2, numbers
      except ValueError:
          print('no numbers in the answer')
          return id+2, answer