# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 16:02:59 2017

@author: SteveJSmith1

name of program: MorseTranslator.py

This program encodes from morse code to
text and decode from text to morse code, either
from strings or files.

See test.py for complete usage details

Usage:
    morseCoder(string=None, file=None, encode=False, decode=False, full=True, save=False)

    Encode a string keeping punctuation:
        morseCoder(string, encode=True)
    Encode a file without punctuation:
        (useful for written speech)
        f = 'your_file.txt'
        morseCoder(file=f, encode=True, full=False)
    Decode a file containing Morse Code:
        morseCoder(string, decode=True)
    Saving output (save=True):
        morseCoder(file=f, encode=True, save=True)
"""




#=============================================

## Morse Alphabet

#=============================================

def coder(letter_list, encode=False, decode=False, save=False):
    """
    The encoding/decoding function, returns
    an encoded/decoded string when passed a list
    of letters.
    Called from morseCoder()
    """
    
    # Dict of {character : Morse} pairs
    
    alphabet = {
            'a' : '.-', 'b' : '-...' , 'c' : '-.-.', 'd' : '-..',
            'e' : '.', 'f' : '..-.', 'g' : '--.', 'h' : '....',
            'i' : '..', 'j': '.---', 'k' : '-.-', 'l' : '.-..',
            'm' : '--', 'n' : '-.', 'o' : '---', 'p' : '.--.',
            'q' : '--.-', 'r' : '.-.', 's' : '...', 't' : '-', 'u' : '..-',
            'v' : '...-', 'w' : '.--', 'x' : '-..-', 'y' : '-.--', 
            'z' : '	--..', '0' : '-----', '1' : '.----', '2':'..---', 
            '3' : '...--', '4' : '....-', '5' : '.....', '6' : '-....', 
            '7' : '--...', '8' : '---..', '9' : '----.', '.' : '.-.-.-',
            ',' : '--..--', ":" : '---...', '?' : '..--..', "'" : '.----.',
            '-' : '-....-', '/' : '-..-.', '(' : '-.--.-', ')' : '-.--.-',
            '"' : '.-..-.', '@' : '.--.-.', '=' : '-...-', '!' : '-.-.--',
            ' ' : '/', '\n' : '/ .-.-'
            }  
    coded = []
    if encode==True:
        for elem in letter_list:
            if elem not in alphabet:
                continue
            else:                
                coded.append(alphabet.get(elem))
        
        coded_string = ' '.join(coded)
        
    elif decode==True:
        # newline character needs to change
        alphabet.pop('\n', None)
        # swap {key:value} pairs
        inverted = {}
        for key, value in alphabet.items():
            inverted[value] = key
        # replace newline character
        inverted['.-.-'] = '\n'
        
        for elem in letter_list:
            if elem not in inverted:
                continue
            else:
                coded.append(inverted.get(elem))
         
                
        coded_string = ''.join(coded)
    else:
        return
            
    
    if save is True:
        return fileSave(coded_string)
    else:
            
        return coded_string

def morseCoder(string=None, file=None, encode=False, decode=False, full=True, save=False):
    # error catch
    if (string is None and file is None):
        print("string or file must be passed")
        return
    # error catch
    if (encode==False and decode==False):
        print("encode=True or decode=True must be set")
        return
    # string operations
    if string is not None:
        if encode==True:
            letter_list = processTxtString(string, full=full)
        elif decode==True:
            letter_list = processMorseString(string)
    # file operations       
    elif file is not None:
        if encode==True:
            text_string = processFile(file)
            letter_list = processTxtString(text_string, full=full)
        elif decode==True:
            morse_string = processFile(file)
            letter_list = processMorseString(morse_string)
    # error catch   
    else:
        print("Unknown Error")
        return 
    # pass the list of letters obtained above
    # to the coder function with the specified
    # arguments
    return coder(letter_list,encode=encode,decode=decode,save=save)
    
def processTxtString(text_string, full=True):
    """
    This is the module that processes the passed
    text string
    
    Use full=False if wishing to process a 
    text_string for removing punctuation, as in         
    speech
    """
    import re
    
    if full != True:
        # strip punctuation
        rem_newline = re.sub(r'[\n]', ' ', text_string)
        rem_punc = re.sub(r'[^\w\s' ']','',rem_newline)
        # create a list of letters
        letter_list = list(rem_punc)
    else:
        # don't strip punctuation
        letter_list = list(text_string)
    # convert to lower case as morse doesn't do case
    return [i.lower() for i in letter_list]
 


def processMorseString(string):
    # Whitespace used as letter seperators
    letter_list = string.split()
    return letter_list





def processFile(file):
    """
    converts a file to a string
    """
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        text_string = f.read()
    return text_string
    

        
def fileSave(string):
    """
    writes a string to file
    
    """
    print("Please enter a filename to save as:")
    file_name = str(input("> ")) + '.txt'
    with open(file_name, 'w', encoding='utf-8', errors='ignore') as file:
            file.write(string)
    return print("File %s" % file_name + " has been created")
    


  