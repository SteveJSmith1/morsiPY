# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 16:02:59 2017

@author: SteveJSmith1

name of program: test.py

This program tests the functions in MorseTranslator

"""


def test():
    from MorseTranslator import morseCoder
    
    print("Testing encoding on a string")
    morseCoder("Cheese! And, Onion?", encode=True, full=True)
    morseCoder("Cheese! And, Onion?", encode=True)
    morseCoder("Cheese! And, Onion?", encode=True, full=False)
    print("pass")
    print("Testing decoding on a string of Morse code")
    string = '- .... . / .--. .-. --- .--- . -.-. - / --. ..- - . -. -... . .-. --. / . -... --- --- -.- / --- ..-. / - .... . / . - .... .. -.-. ... --..-- / -... -.-- / -... . -. . -.. .. -.-. - / -.. . / ... .--. .. -. --- 	--.. .- / .-.- / .-.- - .... .. ... / . -... --- --- -.- / .. ... / ..-. --- .-. / - .... . / ..- ... . / --- ..-. / .- -. -.-- --- -. . / .- -. -.-- .-- .... . .-. . / .- - / -. --- / -.-. --- ... - / .- -. -.. / .-- .. - .... / .-.- .- .-.. -- --- ... - / -. --- / .-. . ... - .-. .. -.-. - .. --- -. ... / .-- .... .- - ... --- . ...- . .-. .-.-.- / / -.-- --- ..- / -- .- -.-- / -.-. --- .--. -.-- / .. - --..-- / --. .. ...- . / .. - / .- .-- .- -.-- / --- .-. / .-.- .-. . -....- ..- ... . '
    morseCoder(string, decode=True)
    print("pass")
    print("Catching errors")
    morseCoder(string)
    morseCoder()
    print("pass")
    
    print("Testing file encoding")
    f = 'test.txt'
    # encoding
    part = morseCoder(file=f, encode=True, full=False)
    full = morseCoder(file=f, encode=True)
    print("pass")
    # decoding
    print("Testing file decoding")
    f = 'morse.txt'
    decoded = morseCoder(file=f, decode=True)
    print("Pass")
    return
    



if __name__ == '__main__': 
    test()
    
