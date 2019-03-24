#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""语音播报功能的实现

使用pyttsx
"""

import pyttsx3

class Speaker:
    """语音播报类
    
    """

    def __init__(self, mute=False):
        self.mute = mute
        self.voice_engine = pyttsx3.init()
        volume = self.voice_engine.getProperty('volume')
        self.voice_engine.setProperty('volume', volume+10)
        # 支持中文
        self.voice_engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0")
    
    def __del__(self):
        #self.voice_engine.endLoop()
        pass
    
    def say(self, text):
        if not self.mute:
            self.voice_engine.say(text)
            self.voice_engine.runAndWait()
    
    def get_property(self, id_str):
        return self.voice_engine.getProperty(id_str)

    def set_property(self, id_str, p):
        return self.voice_engine.setProperty(id_str, p)

if __name__ == '__main__':
    voice = Speaker()
    #voice.set_property("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0")
    #voice.say("我")
    voice.say("I will speak this text")
    voice.say("我将要说这句话")
    pass