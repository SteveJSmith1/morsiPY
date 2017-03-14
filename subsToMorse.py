# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:59:03 2017

@author: SteveJSmith1

subsToMorseBeta.py

This program parses a .srt file, converts
the lines of text to morse code and then
creates an audio file of morse code.

usage: 
    subsToMorse(file, save_file)
    
    where file is the srt file to process
    and save_file is the filename of the output
"""
import re
import datetime
from MorseAudio import writeWav
from MorseAudio import processDot
from MorseAudio import dotFile
from MorseAudio import getDotEquivs
from MorseTranslator import morseCoder
from srtTools import srtParse

def extractTimes(parsed):
    """
    Extracts the start and end time of each subtitle
    group from the parsed file
    """
    # find the lines that contain times
    times = [l for l in parsed if re.search(r'^[0-9][0-9]:', l)]
    # extract the start and end times
    start_times = [time[:12] for time in times]
    end_times = [time[-12:] for time in times]
    return start_times, end_times

    
def getTimedelta(times):
    """
    This function creates time deltas for the
    passed list of times
    """
    time_deltas = []
    # extracting the time periods from the times
    for i in range(len(times)):
        h = int(times[i][:2])
        m = int(times[i][3:5])
        s = int(times[i][6:8])
        ms = int(times[i][-3:])
        #create timedelta object for each
        time_deltas.append(datetime.timedelta(seconds=s, milliseconds=ms, minutes=m, hours=h))
    return time_deltas
    

def subtitleTimings(starts_td, ends_td):
    """
    Extracts the length a subtitle is displayed
    on screen in milliseconds when passed
    the start and end timedeltas
    """
    sub_ms = []
    for i in range(len(starts_td)):
        delta = (ends_td[i]-starts_td[i]).total_seconds()*1000
        sub_ms.append(round(delta))
    return sub_ms

    
def silenceMS(starts_td, ends_td):
    """
    This function uses the time deltas to
    extract periods where subtitles are not 
    on screen, i.e. silence
    """
    silence = []
    # first period of silence
    silence.append(starts_td[0] - datetime.timedelta(0, 0, 0))
    for i in range(1,len(starts_td)):
        silence.append(starts_td[i] - ends_td[i - 1])
     
    silence_ms = [round(i.total_seconds()*1000) for i in silence]
    return silence_ms
 

def processWords(parsed):
    """
    This function fetches the number of lines
    on screen for each time period and creates
    a single string
    """
    # finds all 'word lines' in parsed text
    words = [l for l in parsed if not re.search(r'^[0-9][0-9]:', l) and not re.search(r'^[0-9]+$', l)]
    # replaces lines of '' with \\split\\
    for i in range(len(words)):
        if words[i] == '':
            words[i] = '\\split\\'
    
    # join the lines together
    joined = ' '.join(words)
    # split back into lines using
    processed = joined.split('\\split\\')
    return processed


def encodeList(processed):
    # pass the list to morseCoder
    # full=False strips punctuation
    morse = [morseCoder(str(l), encode=True, full=False) for l in processed]
    return morse
    
    
def dotEquivs(morse):
    """
    Fetches the number of dot equivalents
    for each line of morse
    """
    
    # pass the list to getDotEquivs
    dot_equivs = [getDotEquivs(m) for m in morse]
    return dot_equivs


def dotMS(sub_ms, dot_equivs):
    """
    Calculates the required length of an
    audible 'dot'
    """
    len_dot_ms = []
    for i in range(len(sub_ms)):
        len_dot_ms.append(sub_ms[i]/dot_equivs[i])
    return len_dot_ms


def nFrames(len_dot_ms):
    """
    calculates the number of frames required
    to return from the dot file
    """
    
    framerate, _ , length, _ = processDot(dotFile())
    frames_per_ms = framerate/length

    nframes = [round(frames_per_ms*l) for l in len_dot_ms]
    return nframes


def dotBytes(nframes):
    """
    Creates a bytes object representing the 'dot'
    """
    
    file = dotFile()
    import wave
    dot_bytes = []
    for n in nframes:
        dot_file = wave.open(file, 'rb')
        dot_bytes.append(dot_file.readframes(n))
        dot_file.close()
        
    return dot_bytes


def compileSoundset(dot_bytes):
    """
    returns dot, dash and silences as bytes
    objects
    """
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
    Compiles the bytes for each line of morse code
    using each sound set
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
        
        # bytearray is faster
        complete_bytes = bytearray()
        # applies the correct soundset for each
        # character pair
        for pair in char_pairs:
            if pair in rules:
                complete_bytes += rules.get(pair)
        morse_compiled_bytes.append(bytes(complete_bytes))
    return morse_compiled_bytes
 

def silenceBytes(silence_ms):
    """
    Creates a byte object of zeros
    to be encoded as silence
    """
    
    framerate, _, _, _ = processDot(dotFile())
    
    frames_per_ms = framerate/1000
    silence_bytes = []
    # muliplier by 4 as 4 bits in a ms
    for val in silence_ms:
        sb = bytes(round(frames_per_ms*4*val))
        silence_bytes.append(sb)
        
    return silence_bytes


def completeBytes(silence_bytes, morse_bytes):
    """
    compiles the bytes object of silence and morse
    """
    #bytearray is much faster
    complete = bytearray()
    for i in range(len(silence_bytes)):
        complete += silence_bytes[i]
        complete += morse_bytes[i]
    # convert back to a bytes object
    return bytes(complete)

    
def processTimes(parsed):
    """
    The functions required to process the times
    are collected here
    """
    start_times, end_times = extractTimes(parsed)
    starts_td = getTimedelta(start_times)
    ends_td = getTimedelta(end_times)
    sub_ms = subtitleTimings(starts_td, ends_td)
    silence_ms = silenceMS(starts_td, ends_td)
    return sub_ms, silence_ms, ends_td
    
    
def subsToMorse(file, save_file):
    """
    The main function call
    """
    
    parsed = srtParse(file, word_lines=False, times=False, tokens=False, tokens2=False)
    
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
    
    _,_,_,params = processDot(dotFile())
       
    writeWav(complete_bytes, save_file, params)
    
    audio_file_length = len(complete_bytes)/44100/4
    
    subtitle_length = ends_td[-1].total_seconds()
    afl, sl = audio_file_length, subtitle_length
    lep = (afl-sl)/sl*100
    
    return print('The error in length is %g%%' % lep)

"""    
file = r'D:\Data\Subs\24\Season 1\24.1x01.12am-1am.DVDRip.XViD-FoV.EN.srt'
subsToMorse(file, '24E1Morse.wav')
"""




