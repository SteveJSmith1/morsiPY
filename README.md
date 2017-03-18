# morsiPy
## Tools for Encoding and Decoding Morse Code

### Files:

#### subsToMorse.py

*This program takes subtitles as found in .srt files and converts them to an audio
.wav file of morse code.*

The length of the audio file matches the length that the subtitles are displayed.
Silence is added when no subtitles appear on screen.
Each displayed subtitle is encoded into audio Morse Code which lasts as long as the
subtitle is displayed on the screen.

#### MorseAudio.py

*This program converts a string of text into an audio .wav file of Morse Code*

#### MorseTranslator.py

*This program encodes from morse code to text and decode from text to morse code, either
from strings or files.*

#### srtTools.py

*This program is called from subsToMorse.py to assist in the extraction of subititles
and times*





