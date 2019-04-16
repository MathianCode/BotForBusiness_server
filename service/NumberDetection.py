from dateparser.search import search_dates

import nltk
import sys
import spacy
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import en_core_web_sm
if '/Users/naveen-pt2724/project/common' not in sys.path:
    sys.path.insert(0, '/Users/naveen-pt2724/project/common')
if '/Users/naveen-pt2724/project/service' not in sys.path:
    sys.path.insert(0, '/Users/naveen-pt2724/project/service')
import exceptions
import context
import NumberParser
import ParamDetection
class NumberDetection:

    contexts = None
    paramDetection = None
    actualparams = {}

    def __init__(self):
        self.contexts = context.Context()
        self.paramDetection = ParamDetection.paramDetection()

    compilation = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
                   "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
                   "thirty", "fourty", "fifty", "sixty", "seventy", "eighty", "ninty", "hundred", "thousand", "lakh",
                   "crore", "million", "billion", "trillion"]

    def isWordNumber(self,word):
        if word in self.compilation:
            return True
        return False

    def stage2(self,sentence):
        words = sentence.split(' ')
        numbers, i = list(), 0
        while i < (len(words)):
            if self.isWordNumber(words[i]) is True:
                number = list()
                while i < len(words) and (self.isWordNumber(words[i]) or (words[i] == "and" and words[i - 1] == "hundred")):
                    number.append(words[i])
                    i = i + 1
                if len(number) != 0:
                    answer = NumberParser.numberParser(" ".join(number))
                    self.actualparams[answer] = " ".join(number)
                    numbers.append(answer)
            i = i + 1
        print(numbers)
        return numbers

    def preprocess(self,sent):
        sent = nltk.word_tokenize(sent)
        sent = nltk.pos_tag(sent)
        return sent

    def stage1(self,sentence):
        gram1 = 'phase1: {<CD>}'
        parser = nltk.RegexpParser(gram1)
        ans_p1 = parser.parse(self.preprocess(sentence))
        numbers = list()
        for i in ans_p1:
            if (type(i) != type((1, 2, 3))):
                numbers.append(i[0][0])
        return numbers

    def validateNumber(self,number):
        neglect = ['/','-']
        for neg in neglect:
            if neg in number:
                return False
        if '.' in number and self.paramDetection.validateDate(number) is True:
            return False
        elif number.isdecimal():
            return True
        elif number.isnumeric() is False:
            return False
        return True

    def detectNumber(self,sentence):
        params = self.contexts.getParamsNeeded()
        found = self.contexts.getParamsFound()
        value = self.contexts.getParamsValue()
        position = self.contexts.getParamsPosition()
        samplesentences = self.contexts.getSampleSentences()
        extractList = list()
        Numbers = list()
        pos = 0
        for i in params:
            if i["datatype"] == "Number" and found[pos] == False:
                extract = {}
                extract["name"] = i["name"]
                Numbers.append(i["name"])
                extract["pos"] = pos
                extractList.append(extract)
            pos = pos + 1
        if len(extractList) == 0:
            return []
        else:
            step1 = self.stage1(sentence)
            filter = set()
            if (len(step1) != 0):
                for ind in range(0, len(step1)):
                    result = self.validateNumber(str(step1[ind]))
                    if (result != False):
                        filter.add(step1[ind])
            step2 = self.stage2(sentence)
            if (len(step2) != 0):
                for ind in range(0, len(step2)):
                    result = self.validateNumber(str(step2[ind]))
                    if (result != False):
                        filter.add(str(step2[ind]))
            if (len(filter) == 0):
                return []
            elif (len(filter) == 1 and len(extractList) == 1):
                value[extractList[0]["pos"]] = str(list(filter)[0])
                found[extractList[0]["pos"]] = True
                self.contexts.setParamsValue(value)
                self.contexts.setParamsFound(found)
            elif (self.contexts.getQuestionIndex() is not -1):
                if len(filter) != 0:
                    ind = self.contexts.getQuestionIndex()
                    needed = self.contexts.getParamsNeeded()
                    found = self.contexts.getParamsFound()
                    value = self.contexts.getParamsValue()
                    lists = self.contexts.getQuestionList()
                    for i in range(0, len(needed)):
                        if needed[i]["name"] == lists[ind]["name"]:
                            value[i] = list(filter)[0]
                            found[i] = True
                            break
                    self.contexts.setParamsValue(value)
                    self.contexts.setParamsFound(found)
            else:
                nlp = self.contexts.getNlpModel()
                main_doc = nlp(sentence)
                scores = list()
                for i in samplesentences:
                    search_doc = nlp(i)
                    scores.append(main_doc.similarity(search_doc))
                scores, samplesentences, position = zip(*sorted(zip(scores, samplesentences, position), reverse=True))
                for i in range(0, len(scores)):
                    postagger = self.preprocess(samplesentences[i])
                    sample_patterns, ind = [], 0
                    while ind < len(position[i]):
                        if position[i][ind] in Numbers:
                            pat = ""
                            if (ind - 1 > -1):
                                pat = pat + postagger[ind - 1][1] + ":"
                            # pat=pat+postagger[ind][1]+":"
                            while ind + 1 < len(position[i]) and position[i][ind] == position[i][ind + 1]:
                                ind = ind + 1
                            if (ind + 1 < len(position[i])):
                                pat = pat + postagger[ind + 1][1]
                            sample_pattern = {}
                            sample_pattern["pattern"] = pat
                            sample_pattern["name"] = position[i][ind]
                            sample_patterns.append(sample_pattern)
                        ind = ind + 1
                    inp_postagger = self.preprocess(sentence)
                    for ans in range(0, len(filter)):
                        hasfound = False
                        if list(filter)[ans] in sentence:
                            hasfound = True
                            parcel = sentence.split(' ')
                            val_pos = parcel.index(list(filter)[ans])
                            inp_pattern = ""
                            if (val_pos - 1 > 0):
                                inp_pattern = inp_pattern + inp_postagger[val_pos - 1][1] + ":"
                            # inp_pattern = inp_pattern + inp_postagger[val_pos][1] + ":"
                            if (val_pos + 1 < len(sentence.split(' '))):
                                inp_pattern = inp_pattern + inp_postagger[val_pos + 1][1]
                        else:
                            temp = list(filter)[ans]
                            if int(temp) in self.actualparams:
                                hasfound = True
                                parcel = sentence.split(' ')
                                actual_value = self.actualparams[int(temp)]
                                actual_value_list = actual_value.split(' ')
                                st = parcel.index(actual_value_list[0])
                                ed = parcel.index(actual_value_list[len(actual_value_list) - 1])
                                inp_pattern = ""
                                if (st - 1 > 0):
                                    inp_pattern = inp_pattern + inp_postagger[st - 1][1] + ":"
                                if (ed + 1 < len(sentence.split(' '))):
                                    inp_pattern = inp_pattern + inp_postagger[ed + 1][1]
                        if hasfound is True:
                            for dicti in sample_patterns:
                                if dicti["pattern"] == inp_pattern:
                                    for d in range(0, len(extractList)):
                                        if (extractList[d]["name"] == dicti["name"]):
                                            origin = extractList[d]["pos"]
                                            break
                                    Numbers.remove(dicti["name"])
                                    found = self.contexts.getParamsFound()
                                    value = self.contexts.getParamsValue()
                                    value[origin] = str(list(filter)[ans])
                                    found[origin] = True
                                    self.contexts.setParamsValue(value)
                                    self.contexts.setParamsFound(found)
                                    sample_patterns.remove(dicti)
                                    break

