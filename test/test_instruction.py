import sounddevice as sd
import soundfile as sf
import time

def recording(t):
    time.sleep(t)

    mydata = sd.rec(int(self.samplerate * self.rec_duration), samplerate=self.samplerate,
                    channels=1, blocking=True)
    sf.write(self.filename, mydata, self.samplerate)