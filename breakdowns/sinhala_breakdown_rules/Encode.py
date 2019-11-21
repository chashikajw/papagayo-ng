
class Transliterator:
    line = ""
    enter = ['\r', '\n']
    scheme = {}
    char_repeats = ["^", ":"]
    char_omits = ["m", "w"]
    char_specials = ["෿", ".", ",", "'", "’", "‘", "‛", "\"", "“", "-", "–", "_", ";", 
		  ":", "+", "(", ")", "{", "}", "'", "‒", "—", "­", "´", "‚", "﻿", "෾", "",
		  "[", "]", "?", "<", ">", "=", "*", "&", "^", "%", "$", "#", "@", "!", "~", "|", "\\", "/"]
    char_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    char_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
		  "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
		  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

       
    def encode_scheme(self):
        f= open("Scheme_Enc.txt",'r',encoding='utf-8')
        while(True):
            line = f.readline()
            #print(line)
            if(line == ""):
                break
            key, val = line.split()
            self.scheme[key] = Node(val[0:val.index('*')],val[val.index('*')+1:])
        
        return self.scheme

    def encoder(self,word):
        self.encode_scheme()
        f2 = open("Out.txt", "w",encoding='utf-16')

        str1 = ""
        str2 = ""
        str3 = ""

        str1 = word
        f2.write(str1 + '\t')
        for i in range(len(str1)):
            f2.write('\n' + str1[i])
            f2.write('\t' + str1[i])

            if(str1[i] in self.scheme):
                f2.write('\n' + 'containskey')
                localNode = Node(self.scheme[str1[i]].word,self.scheme[str1[i]].cat)
                f2.write('\n' + localNode.word + " " + localNode.cat)
                
                if(localNode.cat == "m"):
                    if(localNode.word == "x"):
                        str3 = str3
                    else:
                        str3 = str3[0:len(str3)-2]

                if(localNode.word == ""):
                    str3 = str3 + localNode.word
                else:
                    str3 = str3 + localNode.word + "-"

                if(localNode.cat == "c"):
                    if(localNode.word != "x"):
                        str3 = str3 + "@-"

            else:
                f2.write('\n' + "elseeee")
                if(str1[1] in self.char_specials):
                    str3 = str3 + " "
                elif(str1[i] in self.char_numbers):
                    str3 = str3 + str1[i]
                else:
                    if(i>3):
                        last_char = str3[len(str3)-2:len(str3)-1]
                        if(last_char in self.char_repeats): #If the proceeding phone has two chars
                            str3 = str3 + str3[len(str3)-3:len(str3)]
                        elif(last_char in self.char_omits):  #Do not repeat the proceeding phone for these phones
                            str3 = str3[0:len(str3)]
                        else:  #If the proceeding phone has only one char
                            str3 = str3 + str3[len(str3)-2:len(str3)]

        str2 = str2 + str3 + " "

        str3 = ""
        
        f2.close()
      
        rtn_word = str2.strip('-')
        return rtn_word


        

class Node:
    def __init__(self,word,cat):
        self.word = word
        self.cat = cat
    def show(self):
        print("self.word")
        print(self.word)
        print("self.cat")
        print(self.cat)



#!/usr/bin/python
# -*- coding: utf-8 -*-


class Schwa_Analysis:

    line = ''
    enter = ['\r', '\n']
    scheme = {}
    char_numbers = [
        '0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        ]
    char_letters = [
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
        'J',
        'K',
        'L',
        'M',
        'N',
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V',
        'W',
        'X',
        'Y',
        'Z',
        ]

    def char_type(self):
        f = open('Char_Type.txt', 'r', encoding='utf-8')
        while True:
            line = f.readline()

            # print(line)

            if line == '':
                break
            (key, val) = line.split()
            self.scheme[key] = val

        return self.scheme

    def rule_one(self, word):  # // Implements Rule #1 - Replace first syllable schwa with /a/
        phones = word.strip('-').split('-')
        #print(phones)
        trans = ''
        if phones[0] in self.scheme:
            value = self.scheme[phones[0]]
            if value == 'c':
                if len(phones) > 2:
                    if phones[0] == 'k':
                        if phones[1] == '@':
                            if phones[2] != 'r':
                                phones[1] = 'a'
                    elif phones[1] == '@':

                        phones[1] = 'a'

        for phone in phones:
            trans = trans + phone + '-'

        return trans

    def rule_two(self, word):  # Implements Rule #2 - Occurrences with /r/ and /h/
        phones = word.strip('-').split('-')
        trans = ''
        for i in range(1, len(phones)):
            phone = phones[i]

            if phone == 'r':
                if len(phone) > 2:
                    prev_phone = phones[i - 1]
                    prev_type = self.scheme[prev_phone]
                    if prev_type == 'c':
                        if i + 3 < len(phones):
                            next_phone = phones[i + 1]
                            if next_phone == '@':
                                nnext_phone = phones[i + 2]
                                nnext_type = self.scheme[nnext_phone]
                                if nnext_type == 'c':
                                    phones[i + 1] = 'a'

        for phone in phones:
            trans = trans + phone + '-'

        return trans

    def rule_three(self, word):  # // Implements Rule #3 - If /a/, /e/, /ae/, /o/, /@/ is followed by /h/ and /h/ is preceded by /@/
        phones = word.strip('-').split('-')
        trans = ''

        selected_phones = ['a', 'e', 'ae', 'o', '@']

        for i in range(len(phones)):
            phone = phones[i]

            if phone in selected_phones:
                if i + 3 <= len(phones):
                    next_phone = phones[i + 1]
                    if next_phone == 'h':  # If that phone is followed by /h/
                        nnext_phone = phones[i + 2]
                        if nnext_phone == '@':  # If /h/ is preceded by /@/ ????
                            phones[i + 2] = 'a'

        for phone in phones:
            trans = trans + phone + '-'

        return trans

    def rule_four(self, word):
        phones = word.strip('-').split('-')
        trans = ''
    
        for i in range(len(phones)):
            phone = phones[i]
       
            if phone == '@':
                if i + 3 <= len(phones):
                    next_phone = phones[i + 1]
                    nnext_phone = phones[i + 2]
                    
                    next_type = self.scheme[next_phone]
                    nnext_type = self.scheme[nnext_phone]

                    if next_type == 'c' and nnext_type == 'c':  # If the next two phones are consonants
                        phones[i] = 'a'

        for phone in phones:
            trans = trans + phone + '-'

        return trans

    def rule_five(self, word):
        phones = word.strip('-').split('-')
        trans = ''

        selected_phones = ['r', 'b', 't', 'd']

        if len(phones):
            if phones[len(phones) - 2] == '@':
                last_phone = phones[len(phones) - 1]
                if last_phone[0] in self.char_numbers or last_phone[0] \
                    in self.char_letters:
                    print ('Numberr')
                else:
                    if last_phone not in selected_phones:
                        last_type = self.scheme[last_phone]
                        if last_phone == 'c':
                            phones[len(phones) - 2] = 'a'

        for phone in phones:
            trans = trans + phone + '-'

        return trans

    def rule_six(self, word):
        phones = word.strip('-').split('-')
        trans = ''

        selected_phrases = ['yi', 'wu']
        if len(phones) >= 4:
            phone_before_last = phones[len(phones) - 2]
            phone_last = phones[len(phones) - 1]

            phrase = phone_before_last + phone_last

            if phrase in selected_phrases:
                phone = phones[len(phones) - 3]
                if phone == '@':
                    phones[len(phones) - 3] = 'a'
       
        for phone in phones:
            trans = trans + phone + '-'

        return trans

    def rule_seven(self, word):
        phones = word.strip('-').split('-')
        trans = ''

        for i in range(len(phones)):
            phone = phones[i]

            if len(phones) - i > 4:
                if phone == 'k':
                    next_phone = phones[i + 1]
                    if next_phone == '@':
                        nnext_phone = phones[i + 2]
                        if nnext_phone == 'r' or nnext_phone == 'l':
                            nnnext_phone = phones[i + 3]
                            if nnnext_phone == 'u':
                                phones[i + 1] = 'a'

        for phone in phones:
            trans = trans + phone + '-'

        return trans

    def rule_eight(self, word):

        # Implements Rule #8 - If word start's with /kal/ in several words as follows
        # /kal(a:|e:|o:)y/->/k@l(a:|e:|o:)y/
        # /kale(m|h)(u|i)/->/k@le(m|h)(u|i)/
        # /kal@h(u|i)/->/k@l@h(u|i)/
        # /kal@/->/k@l@/

        phones = word.split('-')
        trans = ''

        first_set = ['a:', 'e:', 'o:']
        second_set = ['m', 'h']
        third_set = ['u', 'i']

        if len(phones) >= 5:
            first_phones = phones[0] + phones[1] + phones[2]
            if first_phones == 'kal':
                next_phone = phones[3]
                if next_phone in first_set and phones[4] == 'y':
                    phones[1] = '@'

        if len(phones) >= 6:
            first_phones = phones[0] + phones[1] + phones[2] + phones[3]
            if first_phones == 'kale':
                next_phone = phones[4]
                nnext_phone = phones[5]
                if next_phone in second_set and nnext_phone \
                    in third_set:
                    phones[1] = '@'

            next_phones = phones[0] + phones[1] + phones[2] + phones[3] \
                + phones[4]
            if next_phones == 'kal@h':
                next_phone = phones[5]
                if next_phone in third_set:
                    phones[1] = '@'

        if len(phones) < 5 and len(phones) > 3:
            first_phones = phones[0] + phones[1] + phones[2] + phones[3]
            if first_phones == 'kal@':
                phones[1] = '@'

        for phone in phones:
            trans = trans + phone + '-'

        return trans


def shewa_analyse(word):
    sa = Schwa_Analysis()
    charType = sa.char_type()

    translit_word = sa.rule_one(word)
    translit_word = sa.rule_two(translit_word)
    translit_word = sa.rule_three(translit_word)
    translit_word = sa.rule_four(translit_word)
    translit_word = sa.rule_five(translit_word)
    translit_word = sa.rule_six(translit_word)
    translit_word = sa.rule_seven(translit_word)

    translit_word = sa.rule_eight(translit_word)
  
    rtn_word = translit_word.strip('-').strip()
    return rtn_word









word = "කනවා"
y = Transliterator()
mid_word = y.encoder(word)
phonesStr = shewa_analyse(mid_word)
temp_phonemes = phonesStr.split("-")
temp_phonemes_new = temp_phonemes[:len(temp_phonemes)-1]
#print('****temp_phonemes_new')
#print(temp_phonemes_new)