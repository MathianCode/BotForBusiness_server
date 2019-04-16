from datetime import date, timedelta

import spacy
from dateutil.relativedelta import relativedelta
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import dateparser
import re
import sys
import en_core_web_sm
from dateparser.search import search_dates
if '/Users/naveen-pt2724/project/common' not in sys.path:
    sys.path.insert(0, '/Users/naveen-pt2724/project/common')
import exceptions
import context
class paramDetection:

    contexts = None
    actualparams = {}

    def __init__(self):
        self.contexts = context.Context()

    def dateParser(self,term, val, char):
        if (term == 'this' or char == 'tomorrow'):
            if (char == "day" or char == "today"):
                return date.today()
            elif (char == 'tomorrow'):
                return date.today() + relativedelta(days=+(1 * 1))
            elif (char == "week"):
                return date.today() - timedelta(date.today().weekday())
            elif (char == "month"):
                return date.today().replace(day=1)
            elif (char == "year"):
                return date.today().replace(month=1).replace(day=1)
        elif (term == 'previous' or term == 'last' or term == 'before' or term == 'yesterday'):
            if (char == "day"):
                return date.today() + relativedelta(days=-(val * 1))
            elif (char == 'yesterday'):
                return date.today() + relativedelta(days=-(1 * 1))
            elif (char == "week"):
                return date.today() + relativedelta(days=-(val * 7))
            elif (char == "month"):
                return date.today() + relativedelta(months=-(val * 1))
            elif (char == "year"):
                return date.today() + relativedelta(years=-(val * 1))
        elif (term == 'next' or term == 'upcoming' or term == 'after'):
            if (char == "day"):
                return date.today() + relativedelta(days=+(val * 1))
            elif (char == "week"):
                return date.today() + relativedelta(days=+(val * 7))
            elif (char == "month"):
                return date.today() + relativedelta(months=+(val * 1))
            elif (char == "year"):
                return date.today() + relativedelta(years=+(val * 1))

    def preprocess(self,sent):
        sent = nltk.word_tokenize(sent)
        sent = nltk.pos_tag(sent)
        return sent

    def validateDate(slef,sentence):
        months = {"1": 31, "2": 28, "3": 31, "4": 30, "5": 31, "6": 30, "7": 31, "8": 31, "9": 30, "10": 31, "11": 30,
                  "12": 31}
        result = re.search("^\d{1,2}(/|.|-)\d{1,2}(/|.|-)\d{2,4}$", sentence)
        print(result)
        if result is not None:
            if '-' in sentence:
                test = sentence.split('-')
            elif '/' in sentence:
                test = sentence.split('/')
            elif '.' in sentence:
                test = sentence.split('.')
            part1 = int(test[0])
            part2 = int(test[1])
            print(part1)
            print(part2)
            if ((part1 > 12 and part2 > 12)):
                return False
            elif part1 < 13 and part2 > months[str(part1)]:
                return False
            elif part2 < 13 and part1 > months[str(part2)]:
                return False
            return True
        else:
            result = re.search("^\d{2,4}(/|.|-)\d{1,2}(/|.|-)\d{1,2}$", sentence)
            print(result)
            if (result is not None):
                if '-' in sentence:
                    test = sentence.split('-')
                elif '/' in sentence:
                    test = sentence.split('/')
                elif '.' in sentence:
                    test = sentence.split('.')
                part2 = int(test[1])
                part3 = int(test[2])
                print(part2, part3)
                if ((part2 > 12 and part3 > 12)):
                    return False
                elif part2 < 13 and part3 > months[str(part2)]:
                    # print(part2,part3)
                    return False
                elif part3 < 13 and part2 > months[str(part3)]:
                    return False
                return True
            return False


    def stage1(self,sentence):
        gram1 = 'phase1: {<IN><CD>?<CC|TO>?<CD>}'
        parser = nltk.RegexpParser(gram1)
        ans_p1 = parser.parse(self.preprocess(sentence))
        dates=list()
        for i in ans_p1:
            if (type(i) != type((1, 2, 3)) and len(i) == 4):
                print(str(i[1][0]) + " " + str(i[3][0]))
                dates.append(str(i[1][0]))
                dates.append(str(i[3][0]))
            if (type(i) != type((1, 2, 3)) and len(i) == 2):
                print(str(i[0][0]) + " " + str(i[1][0]))
                dates.append(str(i[1][0]))
        return dates

    def stage2(self,sentence):
        gram2 = 'phase2: {<IN|JJ|DT|RB>?<CD>?<NN|NNP|NNS>}'
        parser = nltk.RegexpParser(gram2)
        ans_p2 = parser.parse(self.preprocess(sentence))
        dates=list()
        for i in ans_p2:
            if (type(i) != type((1, 2, 3)) and len(i) == 3):
                if (type(i[1][0]) != type(3)):
                    continue
                print(self.dateParser(i[0][0], int(i[1][0]), i[2][0]))
                print(str(i[0]) + " " + str(i[1]) + " " + str(i[2]))
                res=str(self.dateParser(i[0][0], int(i[1][0]), i[2][0]))
                dates.append(res)
                self.actualparams[res]=i[0][0]+" "+i[1][0]+" "+i[2][0]
            if (type(i) != type((1, 2, 3)) and len(i) == 2):
                print(self.dateParser(i[0][0], 1, i[1][0]))
                print(str(i[0]) + " " + str(i[1]))
                res=str(self.dateParser(i[0][0], 1, i[1][0]))
                dates.append(res)
                self.actualparams[res]=i[0][0]+" "+i[1][0]
            if (len(i) == 1 and i[0][0] in ["today","tomorrow","yesterday"]):
                print(self.dateParser("this", '', "today"))
                print(i[0][0])
                res=str(self.dateParser("this", '', i[0][0]))
                dates.append(res)
                self.actualparams[res]=i[0][0]
        return dates

    def stage3(self,sentence):
        l1 = search_dates(sentence)
        #search_dates(sentence)[0][1].date()
        if l1 is not None:
            dates = list()
            print(l1[0][1].date())
            dates.append(str(l1[0][1].date()))
            return dates
        return []

    def checkforit(self,pat1,pat2):
        sp=pat2.split(':')
        if sp[0]+":"+sp[1] in pat1 or sp[1]+":"+sp[2] in pat1:
            return True
        return False

    def DetectDates(self,sentence):
        params = self.contexts.getParamsNeeded()
        found = self.contexts.getParamsFound()
        value = self.contexts.getParamsValue()
        position = self.contexts.getParamsPosition()
        samplesentences = self.contexts.getSampleSentences()
        extractList = list()
        datename=list()
        pos=0
        for i in params:
            if i["datatype"]=="Date" and found[pos]==False:
                extract={}
                extract["name"] = i["name"]
                datename.append(i["name"])
                extract["pos"]=pos
                extractList.append(extract)
            pos=pos+1
        if len(extractList)==0:
            return []
        else:
            filter = set()
            step1=self.stage1(sentence)
            if(len(step1)!=0):
                for ind in range(0,len(step1)):
                    result=self.validateDate(str(step1[ind]))
                    if(result!=False):
                        filter.add(step1[ind])
            step2=self.stage2(sentence)
            if(len(step2)!=0):
                for ind in range(0,len(step2)):
                    result=self.validateDate(str(step2[ind]))
                    if(result!=False):
                        filter.add(step2[ind])
            step3=self.stage3(sentence)
            if (len(step3) != 0):
                for ind in range(0, len(step3)):
                    result = self.validateDate(str(step3[ind]))
                    if (result != False):
                        filter.add(step3[ind])
            if(len(filter)==0):
                return []
            elif(len(filter)==1 and len(extractList)==1):
                value[extractList[0]["pos"]]=str(list(filter)[0])
                found[extractList[0]["pos"]]=True
                self.contexts.setParamsValue(value)
                self.contexts.setParamsFound(found)
            elif(self.contexts.getQuestionIndex() is not -1):
                if len(filter)!=0:
                    ind = self.contexts.getQuestionIndex()
                    needed = self.contexts.getParamsNeeded()
                    found = self.contexts.getParamsFound()
                    value = self.contexts.getParamsValue()
                    lists = self.contexts.getQuestionList()
                    for i in range(0,len(needed)):
                        if needed[i]["name"] == lists[ind]["name"]:
                            value[i] = list(filter)[0]
                            found[i] = True
                            break
                    self.contexts.setParamsValue(value)
                    self.contexts.setParamsFound(found)
            else:
                nlp = self.contexts.getNlpModel()
                main_doc = nlp(sentence)
                scores=list()
                for i in samplesentences:
                    search_doc = nlp(i)
                    scores.append(main_doc.similarity(search_doc))
                scores,samplesentences,position=zip(*sorted(zip(scores,samplesentences,position),reverse=True))
                for i in range(0,len(scores)):
                    postagger=self.preprocess(samplesentences[i])
                    sample_patterns,ind=[],0
                    while ind < len(position[i]):
                        if position[i][ind] in datename:
                            pat=""
                            if(ind-1>0):
                                pat=pat+postagger[ind-1][1]+":"
                            #pat=pat+postagger[ind][1]+":"
                            while ind+1 < len(position[i]) and position[i][ind]==position[i][ind+1]:
                                ind=ind+1
                            if(ind+1<len(position[i])):
                                pat=pat+postagger[ind+1][1]
                            sample_pattern = {}
                            sample_pattern["pattern"]=pat
                            sample_pattern["name"]=position[i][ind]
                            sample_patterns.append(sample_pattern)
                        ind=ind+1
                    inp_postagger=self.preprocess(sentence)
                    for ans in range(0,len(filter)):
                        hasfound=False
                        if list(filter)[ans] in sentence:
                            hasfound=True
                            parcel=sentence.split(' ')
                            val_pos=parcel.index(list(filter)[ans])
                            inp_pattern=""
                            if (val_pos - 1 > 0):
                                inp_pattern = inp_pattern + inp_postagger[val_pos - 1][1] + ":"
                            #inp_pattern = inp_pattern + inp_postagger[val_pos][1] + ":"
                            if (val_pos + 1 < len(sentence.split(' '))):
                                inp_pattern = inp_pattern + inp_postagger[val_pos + 1][1]
                        else:
                            temp=list(filter)[ans]
                            if temp in self.actualparams:
                                hasfound = True
                                parcel = sentence.split(' ')
                                actual_value=self.actualparams[temp]
                                actual_value_list=actual_value.split(' ')
                                st=parcel.index(actual_value_list[0])
                                ed=parcel.index(actual_value_list[len(actual_value_list)-1])
                                inp_pattern=""
                                if(st - 1 > 0):
                                    inp_pattern = inp_pattern + inp_postagger[st - 1][1] + ":"
                                if(ed + 1 < len(sentence.split(' '))):
                                    inp_pattern = inp_pattern + inp_postagger[ed + 1][1]
                        if hasfound is True:
                            for dicti in sample_patterns:
                                if dicti["pattern"]==inp_pattern:
                                    for d in range(0,len(extractList)):
                                        if(extractList[d]["name"]==dicti["name"]):
                                            origin=extractList[d]["pos"]
                                            break
                                    datename.remove(dicti["name"])
                                    found = self.contexts.getParamsFound()
                                    value = self.contexts.getParamsValue()
                                    value[origin] = str(list(filter)[ans])
                                    found[origin] = True
                                    self.contexts.setParamsValue(value)
                                    self.contexts.setParamsFound(found)
                                    sample_patterns.remove(dicti)
                                    break
