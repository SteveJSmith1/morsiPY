# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 14:04:38 2017

@author: SteveJSmith1
"""

def parseSRT(file):
    from srtTools import srtParse
    parsed = srtParse(file, word_lines=False, times=False, tokens=False, tokens2=False)
    return parsed
    



def extractTimes(parsed):
    import re
    times = [l for l in parsed if re.search(r'^[0-9][0-9]:', l)]
    start_times = [time[:12] for time in times]
    end_times = [time[-12:] for time in times]
    return start_times, end_times
    


def getTimedelta(times):
    import datetime

    time_deltas = []
    for i in range(len(times)):
        h = int(times[i][:2])
        m = int(times[i][3:5])
        s = int(times[i][6:8])
        ms = int(times[i][-3:])
        time_deltas.append(datetime.timedelta(seconds=s, milliseconds=ms, minutes=m, hours=h))
    return time_deltas
    

def subtitleTimings(starts_td, ends_td):
    
    sub_ms = []
    for i in range(len(starts_td)):
        delta = (ends_td[i]-starts_td[i]).total_seconds()*1000
        sub_ms.append(round(delta))
    return sub_ms




def silenceMS(starts_td, ends_td):
    import datetime
    silence = []
    silence.append(starts_td[0] - datetime.timedelta(0, 0, 0))
    for i in range(1,len(starts_td)):
        silence.append(starts_td[i] - ends_td[i - 1])
     
    silence_ms = [round(i.total_seconds()*1000) for i in silence]
    return silence_ms
    



def processWords(parsed):
    import re

    words = [l for l in parsed if not re.search(r'^[0-9][0-9]:', l) and not re.search(r'^[0-9]+$', l)]
    #append blank line as loop depends upon it
    words.append('')

    split = []
    for i in range(2,len(words)):
        s = []
        if words[i] == '' and words[i-1] != '' and words[i-2] !=2:
            test = words[i-2] + ' ' + words[i-1]
            s.append(test)
        elif words[i] == '' and words[i-1]:
            s.append(words[i-1])
        split.append(s)
        
    processed = [line for line in split if line != []]
    return processed
    


#====================================================



from MorseTranslator import morseCoder

def encodeList(processed):
    morse = [morseCoder(str(l), encode=True, full=False) for l in processed]
    return morse
    


from MorseAudio import getDotEquivs

def dotEquivs(morse):
    dot_equivs = [getDotEquivs(m) for m in morse]
    return dot_equivs




def dotWavFile():
    return 'dot1.wav'
    

def dotMS(sub_ms, dot_equivs):
    len_dot_ms = []
    for i in range(len(sub_ms)):
        len_dot_ms.append(sub_ms[i]/dot_equivs[i])
    return len_dot_ms
    


from MorseAudio import processDot

def nFrames(len_dot_ms):
    framerate, _ , length, _ = processDot(dotWavFile())
    frames_per_ms = framerate/length

    nframes = [round(frames_per_ms*l) for l in len_dot_ms]
    return nframes
    


def dotBytes(nframes):
    file = dotWavFile()
    import wave
    dot_bytes = []
    for n in nframes:
        dot_file = wave.open(file, 'rb')
        dot_bytes.append(dot_file.readframes(n))
        dot_file.close()
        
    return dot_bytes
    




def compileSoundset(dot_bytes):
    sound_sets = []
    for i in range(len(dot_bytes)):
        dash = dot_bytes[i]*3
        silence1 = bytes(len(dot_bytes[i]))
        silence2 = silence1*3
        silence3 = silence1*4
    
        ss = dot_bytes[i], dash, silence1, silence2, silence3
        
        sound_sets.append(ss)
    return sound_sets
    



def morseBytes(morse, sound_sets):
    
    
    """
    
    """
    
    morse_compiled_bytes = []
    for i in range(len(morse)):
        
        morse[i] += ' '
        dot, dash, silence1, silence2, silence3 = sound_sets[i]
        rules = {'--' : dash + silence1,
                 '-.' : dash + silence1,
                 '..' : dot + silence1,
                 '.-' : dot + silence1,
                 '- ' : dash + silence2,
                 '. ' : dot  + silence2,
                 ' /' : dot + silence3
                 }
        char_pairs = [(morse[i][j] + morse[i][j + 1]) for j in range(len(morse[i])-1)]
     
        complete_bytes = bytearray()
    
        for pair in char_pairs:
            if pair in rules:
                complete_bytes += rules.get(pair)
        morse_compiled_bytes.append(bytes(complete_bytes))
    return morse_compiled_bytes
    



def silenceBytes(silence_ms):
    framerate, _, _, _ = processDot(dotWavFile())
    frames_per_ms = framerate/1000
    silence_bytes = []
    for val in silence_ms:
        sb = bytes(round(frames_per_ms*4*val))
        silence_bytes.append(sb)
        
    return silence_bytes
    


def completeBytes(silence_bytes, morse_bytes):
    complete = bytearray()
    for i in range(len(silence_bytes)):
        complete += silence_bytes[i]
        complete += morse_bytes[i]
    return bytes(complete)
 
def processTimes(parsed):
    start_times, end_times = extractTimes(parsed)
    starts_td = getTimedelta(start_times)
    ends_td = getTimedelta(end_times)
    sub_ms = subtitleTimings(starts_td, ends_td)
    silence_ms = silenceMS(starts_td, ends_td)
    return sub_ms, silence_ms, ends_td
    

 
def subsToMorse(file, save_file):
    

    parsed = parseSRT(file)
    sub_ms, silence_ms, ends_td = processTimes(parsed)
    
    processed = processWords(parsed)
    
    morse = encodeList(processed)
    dot_equivs = dotEquivs(morse)
    len_dot_ms = dotMS(sub_ms, dot_equivs)
    nframes = nFrames(len_dot_ms)
    dot_bytes = dotBytes(nframes)
    sound_sets = compileSoundset(dot_bytes)
    morse_bytes = morseBytes(morse, sound_sets)
    
    
    silence_bytes = silenceBytes(silence_ms)
    
    
    complete_bytes = completeBytes(silence_bytes, morse_bytes)
    
    
    from MorseAudio import writeWav
    
    _,_,_,params = processDot(dotWavFile())
       
    writeWav(complete_bytes, save_file, params)
    
    afl = audio_file_length = len(complete_bytes)/44100/4
    
    sl = subtitle_length = ends_td[-1].total_seconds()
    
    lep = (afl-sl)/sl*100
    
    
    return print('The error in length is %g%%' % lep)
    
       

    
    
    
file = r'D:\Data\Subs\24\Season 1\24.1x01.12am-1am.DVDRip.XViD-FoV.EN.srt'
subsToMorse(file, '24E1Morse.wav')





