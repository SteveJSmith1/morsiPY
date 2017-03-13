# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 15:53:13 2017

@author: stevejsmith567@gmail.com

This is a collection of functions to assist in parsing .srt files

# .srt files contain timestamps and the speech displayed for that timestamp

# Requires re and nltk.word_tokenize



srtParse:   Parse a .srt file with several parsing arguments

dirParse:   Parse a directory of .srt files with several parsing arguments and
            an argument to flatten the resulting list of lists
            
filmLength: Extracts the timestamp from the last subtitle

timeAverages: Provides average words spoken per minute and the number of unique
                words per minute
"""


import re


#=============================================

## Single file parsing


def srtParse(srtfile, word_lines=False, times=False, tokens=False, tokens2=False):
    with open(srtfile, encoding='utf-8', errors='ignore') as f:
        
        """
        Parses an .srt file
        
        args: a .srt file
        
        kwargs: 0 or 1 of must be set
        if 0 kwargs set:
            returns a list of all the lines from the file, including timestamps
            
        word_lines = True   # parses a list of lines of dialogue
        times = True    # parses a list of timestamps in the format HH:MM:SS
        tokens = True   # extracts the dialogue as tokens using nltk.word_tokenizer
                        # this splits 'can't' to 'can', "'", 't'
        tokens2 = True  # extracts the dialogue as tokens after removing all
                        punctuation
                        # this turns 'can't' to 'cant' and 'ended.' to 'ended'
        """
 
        line_list = [line.strip() for line in f]
           
        if word_lines==True:
            
            return extWordsFromSrt(line_list)
            
            
        if times == True:
            return extTimesFromSrt(line_list)
        
        if tokens == True:
            words = extWordsFromSrt(line_list)
            return extTokensFromList(words)
            
        if tokens2 == True:
            
            return srtTokens(srtfile)
            
        else:   
            return line_list
 


def extTimesFromSrt(line_list):
    """
    Takes a list containing all the lines in an .srt file
    and extracts the timestamps using REGEX
    """
    times = [l for l in line_list if re.search(r'^[0-9][0-9]:', l)]
    return times
    

    
def extWordsFromSrt(line_list):
    """
    Takes a list containing all the lines in an .srt file
    and extracts the lines of dialogue as items in a list
    """
    words = [l for l in line_list if not re.search(r'^[0-9][0-9]:', l) and not re.search(r'^[0-9]+$', l) and not l == '']
    
    return words
    
def extTokensFromList(word_list):
    """
    Takes a list of the lines of dialogue, converts to a string
    returns tokens created from string using word_tokenize
    """
    word_string = ' '.join(word_list)
    from nltk import word_tokenize
    tokens = word_tokenize(word_string)
    return tokens
    


def srtTokens(srtFile):
    """
    Takes a .srt file and parses tokens directly after stripping
    punctuation.
    Also called by srtParse(srtFile, tokens=True)
    """
    
    string_lines = srtParse(srtFile, word_lines=True)
    string = ' '.join(string_lines)
    rem_punc = re.sub(r'[^\w\s]','',string)
    return rem_punc.split()
    
#--------------------------------------------------
"""
f = r'D:\Data\Subs\24\24.1x02.1am-2am.DVDRip.XViD-FoV.EN.srt'
srtTokens(f)
# equivalent to
srtParse(f, tokens2=True)
#--------------------------------------------------
f = r'D:\Data\Subs\24\24.1x02.1am-2am.DVDRip.XViD-FoV.EN.srt'
srtParse(f, word_lines=True)
srtParse(f, times=True)
srtParse(f, tokens=True)
"""
#---------------------------------------------------




#============================================

## Parsing operations upon a directory

def getFilenames(rootDir):
    """ Returns a list of .srt files in a directory """
    import os
    filelist = os.listdir(rootDir)
    return [rootDir + "\\" + i for i in filelist if i.endswith('srt')]
    
#----------------------------------------
"""
fullpaths = getFilenames(r'D:\Data\Subs\24')
"""
#----------------------------------------


def dirParse(rootDir, word_lines=False, times=False, tokens=False, tokens2=False, flat=False):
    file_list = getFilenames(rootDir)
    """
    Passes a directory to individual calls of srtParse()
    
    args: a directory
        
        kwargs: 0 or 1 of must be set
        if 0 kwargs set:
            returns a list of all the lines from the file, including timestamps
            
        word_lines = True   # parses a list of lines of dialogue for each file
        times = True    # parses a list of timestamps in the format HH:MM:SS for each               
                        # file
        tokens = True   # extracts the dialogue as tokens using nltk.word_tokenizer
                        # for each file
                        # this splits 'can't' to 'can', "'", 't'
        tokens2 = True  # extracts the dialogue as tokens after removing all
                        punctuation for each file
                        # this turns 'can't' to 'cant' and 'ended.' to 'ended'
                        
        flat = True     # flattens the resulting list of lists e.g. to acquire 
                        # all dialogue for a series in a single list
    """                  
        
    if flat==True:
        listoflists = [srtParse(i, word_lines=word_lines, times=times, tokens=tokens, tokens2=tokens2) for i in file_list]
        return flatten(listoflists)
        
    else:
        return [srtParse(i, word_lines=word_lines, times=times, tokens=tokens, tokens2=tokens2) for i in file_list]
        
#-------------------------------
"""
root = r'D:\Data\Subs\24'
dirParse(root, tokens2=True)
"""
#-------------------------------


def flatten(listOflists):
    """
    Takes a list of lists and flattens.
    Usage: To merge individual extractions from a list of file
    """
    
    return [item for sublist in listOflists for item in sublist]

#--------------------------------------------
"""
root = r'D:\Data\Subs\24'
dirParse(root, tokens2=True, flat=True)[-10:]
"""
#--------------------------------------------



#============================================
def seriesParse(rootDir, word_lines=False, times=False, tokens=False, tokens2=False, flat=False):
    """
    Given a root directory, this function passes each immediate subdirectory
    to the dirParse() function with the specified kwargs
    
    directory structure should be of form
    r'D:\Data\Subs\24

    with seasons in sub folders such as

    r'D:\Data\Subs\24\Season 1
    r'D:\Data\Subs\24\Season 2
    etc
    
    args: a directory
        
        kwargs: 0 or 1 of must be set
        if 0 kwargs set:
            returns a list of all the lines from the file, including timestamps
            
        word_lines = True   # parses a list of lines of dialogue for each file
        times = True    # parses a list of timestamps in the format HH:MM:SS for each               
                        # file
        tokens = True   # extracts the dialogue as tokens using nltk.word_tokenizer
                        # for each file
                        # this splits 'can't' to 'can', "'", 't'
        tokens2 = True  # extracts the dialogue as tokens after removing all
                        punctuation for each file
                        # this turns 'can't' to 'cant' and 'ended.' to 'ended'
                        
        flat = True     # flattens the resulting list of lists e.g. to acquire 
                        # all dialogue for a series in a single list
    """         
    
    import os
    dirs = [x[0] for x in os.walk(rootDir)]
    season_dirs = [dirs[i] for i in range(1, len(dirs))]
    season_names = [os.path.split(path)[1] for path in season_dirs]
    print('-'*30)
    print("This may take some time")
    print('-'*30)
    series_parse = []
    for path in season_dirs:
        index = season_dirs.index(path)
        print('-'*30)
        print('Parsing %s...' % season_names[index])
        series_parse.append(dirParse(path, word_lines=word_lines, times=times, tokens=tokens, tokens2=tokens2, flat=flat))
    print('-'*30)
    print('Parsing complete!')
    print('-'*30)
    return series_parse
    

    


#===========================================

## Tools to extract data based on the timestamps
## in the files

#============================================
    
def filmLength(srtFile):
    """
    Extracts a timestamp for the last line of dialogue in an srtFile
    """
    times = srtParse(srtFile, times=True)
    length_of_prog = times[-1][-12:-4]

    return length_of_prog
   

#============================================
"""

f = r'D:\Data\Subs\24\24.1x02.1am-2am.DVDRip.XViD-FoV.EN.srt'
filmLength(f)
#----------------------------------------------
root = r'D:\Data\Subs\24'
fullpaths = getFilenames(root)

lengths = [filmLength(i) for i in fullpaths]
lengths
#-----------------------------------------------
"""


#============================================

def timeAverages(srtFile):
    """
    input: an .srt file
    returns a list [filename, Words spoken per minute, Unique words spoken per minute]
    
    
    """
    length_of_prog = filmLength(srtFile)
    hours = int(length_of_prog[0:2])
    minutes = int(length_of_prog[3:5])
    seconds = int(length_of_prog[6:8])
    
    
    len_minute = hours*60 + minutes + seconds/60
    
    
    words = srtParse(srtFile, tokens=True)
    num_of_words = len(words)
    
    print("""
    For the srt file with filename:
        %s""" % srtFile)
    # words per minute

    wpm = num_of_words/len_minute
    print('Words spoken per minute: %.2f' % wpm)
    #unique words per minute
    
    unique_words = len(set(words))
    uwpm = unique_words / len_minute
    print('Unique words spoken per minute: %.2f' % uwpm)
    aves = [srtFile, wpm, uwpm]
    return aves

#=============================================

"""
timeAverages(f)

['D:\\Data\\Subs\\24\\24.1x02.1am-2am.DVDRip.XViD-FoV.EN.srt',
 101.22042341220424,
 20.523038605230386]
"""
#-----------------------------------------------
"""
root = r'D:\Data\Subs\24'
fullpaths = getFilenames(root)

[timeAverages(i) for i in fullpaths]
#------------------------------------------------
"""




