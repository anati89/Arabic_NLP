"""
This module implements functions to:
1. Strip harakat
2. Replace shaddah with duplicating previous letter
# reference for utf-8 mapping table:
#http://utf8-chartable.de/unicode-utf8-table.pl?start=1536&utf8=string-literal
"""
import sys
import re
import binascii

HARAKAT = {
    'FATHA': r'\xd9\x8e',
    'FATHATAN': r'\xd9\x8b',
    'DAMMA': r'\xd9\x8f',
    'DAMMATAN': r'\xd9\x8c',
    'KASRA': r'\xd9\x90',
    'KASRATAN': r'\xd9\x8d',
    'SUKUN': r'\xd9\x92',
    'TATWEEL': r'\xd9\x80'
}

EXTRA_LETTERS = {
    'ALTAREEF': r'\xd8\xa7\xd9\x84'#
}

SHADDA = r'\xd9\x91'

ALL_HARAKAT = '|'.join([part.replace('\\', '\\\\') for part in HARAKAT.values()])


class Word:
    """
    This class represents word and related methods
    """
    def __init__(self, word):
        """
        Initialize encoded word, length, etc ..
        :param word:
        """
        self.word = word
        self.shaddah_hex = SHADDA.replace('\\x', '')
        self.encoded_word = str(self.word.encode(encoding="utf-8"))
        self.decoded_word, self.shaddah = self.strip_harakat()
        self.enc_length = self.__len__() # length of encoded not word itself. word is length of encoded / 2
        self.length = self.enc_length // 2
        self.remove_shaddah()

    def strip_harakat(self):
        """
        This func is used to remove harakat from given word
        :param word:
        :return:decoded_word, shaddah
        """
        self.encoded_word = re.sub(ALL_HARAKAT, '', self.encoded_word)
        self.encoded_word = self.encoded_word[2:-1]
        shaddah = None
        shaddah = SHADDA in self.encoded_word
        # TODO: Assume that word has more than 1 shaddah ..
        self.encoded_word = self.encoded_word.replace('\\x', '')
        if shaddah:
            before_shaddah = self.encoded_word.split(self.shaddah_hex)[0]
            to_duplicated = ''.join(before_shaddah[-4:])
            self.encoded_word = re.sub(self.shaddah_hex, to_duplicated, self.encoded_word)
        self.encoded_word = binascii.a2b_hex(self.encoded_word)
        decoded_word = self.encoded_word.decode('utf8')
        self.encoded_word = str(self.encoded_word)
        return decoded_word, shaddah

    def decode_word(self, word):
        """
        Take hex word with b' prefex and return decoded one
        :param word:
        :return:  decoded_word
        """
        word = str(word)[2:-1]
        word = word.replace('\\x', '')
        word = binascii.a2b_hex(word)
        decoded_word = word.decode('utf8')
        return decoded_word

    def remove_shaddah(self):
        """
        remove shaddah if length of word > 3 and has shaddah
        :return: encoded_word
        """
        if self.length > 3 and self.shaddah:
            self.encoded_word = re.sub(self.shaddah_hex, '', self.encoded_word)

        self.decoded_word =self. decode_word(self.encoded_word)

    def __len__(self):
        """return length of encoded word"""
        self.length = self.encoded_word.count('\\x')
        return self.length


word = 'كـَأنَّها'
word_obj = Word(word)
print(word_obj.encoded_word)
print(word_obj.decoded_word)
print(word_obj.length)

word = "يُغَنّي"
word_obj1 = Word(word)
print('encoded_word: ', word_obj1.encoded_word)
print('decoded_word: ', word_obj1.decoded_word)
print('length: ', word_obj1.length)


word = "كُفؤٌ"
word_obj1 = Word(word)
print('encoded_word: ', word_obj1.encoded_word)
print('decoded_word: ', word_obj1.decoded_word)
print('length: ', word_obj1.length)

word = "غَلَّ"
word_obj1 = Word(word)
print('encoded_word: ', word_obj1.encoded_word)
print('decoded_word: ', word_obj1.decoded_word)
print('length: ', word_obj1.length)
print('after removing shaddeh: ', word_obj1.remove_shaddah())

sys.exit()
text1 = "ا"
text2 = "ب"
text3 = "َ"
text4 = 'بَ'
text5 = "با"
dec = text4.encode(encoding="utf-8")
print('text 1 encoded: ', text1.encode(encoding="utf-8"))
print('text 2 encoded: ', text2.encode(encoding="utf-8"))
print('text 3 encoded: ', text3.encode(encoding="utf-8"))
print('text 4 encoded: ', text4.encode(encoding="utf-8"))
print(text3.encode(encoding="utf-8"), dec.decode(encoding='utf-8'))
print('text 5 encoded: ', text5.encode(encoding="utf-8"))
