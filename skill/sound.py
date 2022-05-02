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
from neon_utils.skills.neon_skill import NeonSkill
import re
import sounddevice as sd
import soundfile as sf
import wavfile
from neon_tts_plugin_coqui_ai import CoquiTTS
from neon_stt_plugin_polyglot import PolyglotSTT
import pyttsx3
import time


# import required module
import os


class Audio(NeonSkill):

    def __init__(self, bus, lang):
        super().__init__(name='Audio', bus=bus)
        self.samplerate = 16000
        self.rec_duration = 4 #recording seconds
        self.filename = 'output.wav'
        self.lang = lang or 'en'
    #
    # def communication(self,  text, question_id):
    #     answer = self.get_response(text)
    #     return

    def recording(self, t):
        time.sleep(t)

        mydata = sd.rec(int(self.samplerate * self.rec_duration), samplerate=self.samplerate,
                        channels=2, blocking=True)
        sf.write(self.filename, mydata, self.samplerate)

    def call_stt(self):
        stt = PolyglotSTT(self.lang)
        result = stt.execute(self.filename)
        answer_no_punct = re.sub('[^0-9a-zA-Z\s]+', '', result.lower())
        return answer_no_punct

    def calculate_audio_length(file):
        # calculate the wav file lenght (seconds)
        Fs, data = wavfile.read(file)
        n = data.size
        time_wait = n / Fs
        print("waiting time before listening to user's answer: ", time_wait)
        return time_wait

    def call_tts_pyttsx3(self, text, id):
        '''
        calls tts pyttsx3 module
        converts text from jsonl file into audio
        calculates the audio file lenth in seconds
        displays created audio file
        :param text: input text to speak -> str
        :param id: question id for file creation -> str
        returns audio file length in seconds -> int
        '''
        file_name = 'audio' + id + '.wav'
        engine = pyttsx3.init() #start pyttsx3 engine
        if self.lang == 'en':
            engine.setProperty('voice', "english")
        elif self.lang == 'pl':
            engine.setProperty('voice', "polish")
        engine.save_to_file(text, file_name)
        # time.sleep(5)
        time_wait = Audio.calculate_audio_length(file_name)
        os.system("mpg123 " + file_name) #play audio
        engine.stop() #stop pyttsx3 engine
        return time_wait

    def call_tts_qocui(self, text, question_id):
        file_name = 'audio' + question_id + '.wav'
        coquiTTS = CoquiTTS(self.lang)
        coquiTTS.get_tts(text, file_name)
        time_wait = Audio.calculate_audio_length(file_name)
        os.system("mpg123 " + file_name) #play audio
        return time_wait

    def repeat(self, question_id):
        if self.lang == 'en':
            text = 'Repeat, please'
            self.call_tts_qocui(self, text, question_id)
        elif self.lang == 'pl':
            text = 'Powtórz, proszę..'
            self.call_tts_qocui(self, text, question_id)
        else:
            text = 'Повторіть, будь-ласка.'
            self.call_tts_qocui(self, text, question_id)

    def no_instructions(self):
        if self.lang == 'en':
            text = 'No instructions for this case.'
            question_id = '0'
            self.call_tts_qocui(self, text, question_id)
        elif self.lang == 'pl':
            text = 'Brak struktury dla tej sprawy.'
            question_id = '0'
            self.call_tts_qocui(self, text, question_id)
        else:
            text = 'Немає інструкцій для цього випадку.'
            question_id = '0'
            self.call_tts_qocui(self, text, question_id)

    def finish(self):
        if self.lang == 'en':
            text = 'Finished'
            question_id = '0'
            self.call_tts_qocui(self, text, question_id)
        elif self.lang == 'pl':
            text = 'Skończone'
            question_id = '0'
            self.call_tts_qocui(self, text, question_id)
        else:
            text = 'Закінчили'
            question_id = '0'
            self.call_tts_qocui(self, text, question_id)


