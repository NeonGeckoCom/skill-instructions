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