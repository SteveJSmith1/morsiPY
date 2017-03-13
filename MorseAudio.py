
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 16:02:59 2017

@author: SteveJSmith1

name of program: 


This program will 
Usage: 
"""



# v 0.1

import wave


def processDot(file):
    """
    Fetches parameters from the wave file
    used to represent a dot
    """
    wav_file = wave.open(file, 'rb')
    params = wav_file.getparams()
    framerate = wav_file.getparams()[2] 
    nframes =wav_file.getparams()[3]
    length_wav = nframes / (framerate/1000)
    wav_file.close()
    return framerate, nframes, length_wav, params
    

def dotBytes(file, ms):
    """
    Fetches framerate and length returned from
    processDot to read the number of frames
    required to have dot length of the milliseconds
    specified
    """
    framerate, _ , length, _ = processDot(file)
    frames_per_ms = framerate/length
    nframes = frames_per_ms*ms
    
    if ms <= length:
        wav_file = wave.open(file, 'rb')
        wav_bytes = wav_file.readframes(int(nframes))
        wav_file.close()
        
    else:
        print("File is only %s ms in length" % length)
        return
    
    return wav_bytes
    
def soundSet(file, dot_ms):
    """
    Creates a soundSet of dot, dashes and
    silences as byte objects
    """
    dot = dotBytes(file, dot_ms)
    dash = dot*3
    silence1 = bytes(len(dot))
    silence2 = silence1*3
    silence3 = silence1*4
    
    sound_set = dot, dash, silence1, silence2, silence3
    return sound_set

def getDotEquivs(morse_string):   
    morse_string += ' '
    char_pairs = [(morse_string[i] + morse_string[i + 1]) for i in range(len(morse_string)-1)]
     
    rules = { '--' : 4, '-.' : 4, '..' : 2,
             '.-' : 2, '- ' : 6, '. ' : 4, ' /' : 5
             }
    pair_dotequivs = [rules.get(pair) for pair in char_pairs if pair in rules]
    return sum(pair_dotequivs)

def completeBytes(dot_file, morse_string, ms=100):
    """
    
    """
    morse_string += ' '
    dot, dash, silence1, silence2, silence3 = soundSet(dot_file, ms)
    
    rules = {'--' : dash + silence1,
             '-.' : dash + silence1,
             '..' : dot + silence1,
             '.-' : dot + silence1,
             '- ' : dash + silence2,
             '. ' : dot  + silence2,
             ' /' : dot + silence3
             }
    char_pairs = [(morse_string[i] + morse_string[i + 1]) for i in range(len(morse_string)-1)]
     
    complete_bytes = bytes()
    
    for pair in char_pairs:
        if pair in rules:
            complete_bytes += rules.get(pair)
    
    return complete_bytes
    
#------------------------------------------

#==========================================

def morseToWav(dot_file, morse_string, save_file, ms=100):
    
        
    wav_file = completeBytes(dot_file,morse_string, ms)
    file = wave.open(dot_file, 'rb')
    params = file.getparams()   
    new_params = (params[0], params[1], params[2], None, 'NONE', None)      
    file.close()
    writeWav(wav_file, save_file, new_params)
    
    return 
    
def writeWav(wav_file, save_file, params):
    
    f = wave.open(save_file, 'wb') 
    f.setparams(params)
    f.writeframesraw(bytes(wav_file))
    f.close()
    return 
 
    
#=============================================

def fixMs(morse_string, required_length):
    dot_equivs = getDotEquivs(morse_string)
    ms = required_length/dot_equivs
    return ms
    
#==============================================

def txtToMorseWav(string, full=True, ms=None, length=None, file='temp.wav'):
    from MorseTranslator import morseCoder
    morse_string = morseCoder(string, encode=True, full=full)
    if (length is not None and ms is None):
        ms = fixMs(morse_string, length)
    elif (length is None and ms is not None):
        pass
    elif (length is None and ms is None):
        print('ms or length needs to be passed')
        return
        
    return morseToWav(dotFile(), morse_string, file, ms)
    
def txtToBytes(string, full=True, ms=None, length=None):
    from MorseTranslator import morseCoder
    morse_string = morseCoder(string, encode=True, full=full)
    if (length is not None and ms is None):
        ms = fixMs(morse_string, length)
    elif (length is None and ms is not None):
        pass
    elif (length is None and ms is None):
        print('ms or length needs to be passed')
        return
        
    return completeBytes(dotFile(), morse_string, ms)
    
def dotFile():
    return 'dot1.wav'
    
def writeSilence(length):
    _,_,_,params = processDot(dotFile())
    silence = bytes(int((params[2]*(length/1000))))  
    
    return silence
    
#===================================

def readWav(file):
    
   
    wav_file = wave.open(file, 'rb')
    nframes = wav_file.getnframes()
    wav_bytes = wav_file.readframes(int(nframes))
    wav_file.close()
     
    return wav_bytes

