import sys
import collections
from pymongo import MongoClient
import math
from service import ParamDetection
from service import NumberDetection
import dateparser
from dateparser.search import search_dates
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
# import en_core_web_md
# import en_core_web_lg
nlp = en_core_web_sm.load()
if '/Users/naveen-pt2724/project/common' not in sys.path:
    sys.path.insert(0, '/Users/naveen-pt2724/project/common')
import exceptions
import context
class ActionDetection:
    userid = None
    contexts = None
    DBSentences = None
    ParamsNeeded = list()
    ActionNames = list()
    IsString = list()

    def getUserDBconnection(self):
        client = MongoClient("mongodb://127.0.0.1:27017")
        database=client.BFB
        operation=database.user
        return operation
    def getSampleSentences(self):
        self.contexts = context.Context()
        self.userid = self.contexts.getApiKey()
        operations=self.getUserDBconnection()
        data=operations.find({"_id":self.userid})
        if(data.count()==0):
            raise exceptions.InvalidApiKey("Invalid ApiKey")
        else:
            data_dict={}
            for i in data:
                data_dict=i
            SampleSentences=list()
            for i in range(0,len(data_dict["actions"])):
                gather=list()
                isstring=list()
                if(len(data_dict["actions"])!=0):
                    self.ActionNames.append(data_dict["actions"][i]["name"])
                    self.ParamsNeeded.append(data_dict["actions"][i]["param_def"])
                    for j in range(0,len(data_dict["actions"][i]["sentence_def"])):
                        gather.append(data_dict["actions"][i]["sentence_def"][j]["sentence"].strip())
                        isstring.append(data_dict["actions"][i]["sentence_def"][j]["isstring"])
                SampleSentences.append(gather)
                self.IsString.append(isstring)
            print(SampleSentences)
            self.DBSentences=SampleSentences
        return SampleSentences


    def findAction(self,sentence):
       SampleSentences = self.getSampleSentences()
       SampleSentences_TF=[]
       IDF_set=set()
       SampleSentences_Token=[]
       for SampleSentence in SampleSentences:
           temp=[]
           for document in SampleSentence:
               for word in document.split(' '):
                   IDF_set.add(word)
                   temp.append(word)
           TF=collections.Counter(temp)
           SampleSentences_Token.append(temp[:])
           for k in list(TF):
               TF[k]=TF[k]/len(temp)
           SampleSentences_TF.append(TF)
       IDF={}
       for i in IDF_set:
           count=0
           for Token in SampleSentences_Token:
               if i in Token:
                   count=count+1
           IDF[i]=1+math.log(len(SampleSentences_Token)/count,2.71828)
       Target = sentence.split(' ')
       Target_TF=collections.Counter(Target)
       Target_set=set(Target)
       comp=[]
       for i in Target_set:
           if i in IDF:
               comp.append(Target_TF[i]*IDF[i])
           else:
               comp.append(0)

       Sentence_vector=[]
       for i in range(0,len(SampleSentences_Token)):
           Sentence_vector.append([])
       for i in Target_set:
           for j in range(len(SampleSentences_Token)):
               if i in SampleSentences_Token[j] and IDF:
                   Sentence_vector[j].append(SampleSentences_TF[j][i]*IDF[i])
               else:
                   Sentence_vector[j].append(0)

       scores=[]
       for i in range(0,len(Sentence_vector)):
           doc=Sentence_vector[i]
           summ,q,d = 0,0,0
           for j in range(0,len(doc)):
               summ=summ+(comp[j]*doc[j])
               q = q + (comp[j] ** 2)
               d = d + (doc[j] ** 2)
           d1b = math.sqrt(d)
           q1b = math.sqrt(q)
           cos=0
           if q1b*d1b!=0:
               cos = summ / (q1b * d1b)
           scores.append(cos)
       print(scores)
       maximum_score=max(scores)
       if(maximum_score>0.49):
           pos=scores.index(maximum_score)
           self.contexts.setActionDetected(self.ActionNames[pos])
           self.contexts.setParamsNeeded(self.ParamsNeeded[pos])
           self.contexts.setSampleSentences(self.DBSentences[pos])
           self.contexts.setParamsPosition(self.IsString[pos])
           found = [False]*len(self.ParamsNeeded[pos])
           value = [0]*len(self.ParamsNeeded[pos])
           self.contexts.setParamsValue(value)
           self.contexts.setParamsFound(found)
           print("Action detected is : "+self.ActionNames[pos])
           findParams = ParamDetection.paramDetection()
           findParams.DetectDates(sentence)
           findParams = NumberDetection.NumberDetection()
           findParams.detectNumber(sentence)
       else:
           print("Sorry!! cannot understand")
           raise exceptions.ActionNotFound("Action Not Found")





