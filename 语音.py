import pyautogui
import os.path
import  pyttsx3
import pyaudio
import  wave
from aip import AipSpeech
import os
import  keyboard
import time
import win32api
import win32con
def text2video(line):
  engine = pyttsx3.init()
  #调整频率
  rate = engine.getProperty('rate')
  engine.setProperty('rate', rate-10)
  # 调整音量
  volume = engine.getProperty('volume')
  engine.setProperty('volume', volume)
  engine.say(line)
  engine.runAndWait()

class collect_video:
  CHUNK = 512
  FORMAT = pyaudio.paInt16
  CHANNELS = 1
  RATE = 16000

  def __init__(self):
    self.paudio = None
    self.stream = None

  def open(self):

    self.paudio = pyaudio.PyAudio()
    self.stream = self.paudio.open(format=self.FORMAT,
                                   channels=self.CHANNELS,
                                   rate=self.RATE,
                                   input=True,
                                   frames_per_buffer=self.CHUNK)

  def read(self):
    data = self.stream.read(self.CHUNK)
    return data

  def read_s(self, time=1):
      data = []
      T = self.RATE // self.CHUNK * time
      text2video("录音开始")
      for i in range(T):
          data.append(self.stream.read(self.CHUNK))
      text2video("录音结束")
      return data

  def close(self):
    self.stream.close()
    self.paudio.terminate()

  def save(self, filename='qr.wav', data=[]):
    wf = wave.open(filename, "wb")
    wf.setnchannels(self.CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(self.RATE)
    wf.writeframes(b"".join(data))
    wf.close()

  def play(self, path="qr.wav"):
    # 定义数据流块
    chunk = 1024
    # 只读方式打开wav文件
    f = wave.open(path, "rb")
    # 打开数据流
    fstream = self.paudio.open(format=self.paudio.get_format_from_width(f.getsampwidth()),
                               channels=f.getnchannels(),
                               rate=f.getframerate(),
                               output=True)
    # 读取数据
    data = f.readframes(chunk)
    # 播放
    while data:
      fstream.write(data)
      data = f.readframes(chunk)
    # 停止数据流
    fstream.stop_stream()
    fstream.close()

def video2text1():
  a = collect_video()
  a.open()
  data = a.read_s(8)
  a.save(data=data)
  a.close()
  APP_ID ='22098155'
  API_KEY = 'V7iAEqpEODLxCIiA7GwN2819'
  SECRET_KEY = 'wrbkfGWmPywYHHTKaLNo2G8uhgrqkcx7'
  client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
  result = client.asr(get_file_content('qr.wav'), 'wav', 16000, {
  'dev_pid': 1537, })
  text = result['result'][0]
  return text

def get_file_content(filePath):
  with open(filePath, 'rb') as fp:
    return fp.read()


class PinYin(object):
    def __init__(self, dict_file='word.data'):
        self.word_dict = {}
        self.dict_file = dict_file

    def load_word(self):
        if not os.path.exists(self.dict_file):
            raise IOError("NotFoundFile")

        with open(self.dict_file) as f_obj:
            for f_line in f_obj.readlines():
                try:
                    line = f_line.split('    ')
                    self.word_dict[line[0]] = line[1]
                except:
                    line = f_line.split('   ')
                    self.word_dict[line[0]] = line[1]

    def hanzi2pinyin(self, string=""):
        result = []
        if not isinstance(string, str):
            string = string.decode("utf-8")

        for char in string:
            key = '%X' % ord(char)
            result.append(self.word_dict.get(key, char).split()[0][:-1].lower())

        return result

    def hanzi2pinyin_split(self, string="", split=""):
        result = self.hanzi2pinyin(string=string)
        if split == "":
            return result
        else:
            return split.join(result)



p=PinYin()
p.load_word()
def speak(lxy):
    lxy=p.hanzi2pinyin(lxy)
    qr=""
    for i in lxy:
        qr=qr+i
    qr=qr+'1'
    keyboard.press("enter")
    keyboard.release("enter")
    time.sleep(0.3)
    pyautogui.write(qr, interval=0.01)
    keyboard.press("enter")
    keyboard.release("enter")



wrong=['操','草','妈','逼','麻','死','狗','日','贱','杂','猪','傻','屌','鸡','脑','残','瘫','智','干','上']
def judge(name):
    Judge=1
    for i in wrong:
        if(i==name):
            Judge=0
    return Judge




def Speak():
    final = []
    keyboard.wait('t')
    name=video2text1()
    j=0
    for i in range(0,len(name)):
        if(judge(name[i])==0):
            if(j==i):
                final.append(name[i])
            else:
                ans=name[j:i]+name[i]
                final.append(ans)
            j=i+1
        elif(i==len(name)-1):
            if (j == i):
                final.append(name[i])
            else:
                ans = name[j:i] + name[i]
                final.append(ans)
    text2video('可以发送了')
    keyboard.wait('t')
    time.sleep(0.3)
    for i in range(0,len(final)):
        try:
            speak(final[i])
            if(i==(len(final)-1)):
                pass
            else:
                time.sleep(0.2)
        except:
            text2video("请好好说纯中文")

while(1):
    Speak()
