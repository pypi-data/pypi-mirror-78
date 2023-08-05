# n0translate.translit_dict
n0translate.translit_dict is a dictionary for Python3 str.translate(dict) allows to translit cyrillic/french/spanish and other latin like languages from UTF-8 into ASCII-7 encoding.
Transliteration is the process of transferring a word from the alphabet of one language to another. 
It changes the letters from the word's original alphabet to similar-sounding letters in a different one.
Transliteration helps people pronounce words and names in foreign languages.
Usage:
import n0translate
dst_str = src_str.translate(n0translate.translit_dict)

