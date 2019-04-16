from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import en_core_web_sm
import sys
if '/Users/naveen-pt2724/project/common' not in sys.path:
    sys.path.insert(0, '/Users/naveen-pt2724/project/common')
if '/Users/naveen-pt2724/project/service' not in sys.path:
    sys.path.insert(0, '/Users/naveen-pt2724/project/service')
import exceptions
import context

class StringDetection:

    contexts = None

    def __init__(self):
        self.contexts = context.Context()

    def detectString(self,sentence):
        if len(sentence) is not 0:
            params = self.contexts.getParamsNeeded()
            found = self.contexts.getParamsFound()
            value = self.contexts.getParamsValue()
            position = self.contexts.getParamsPosition()
            samplesentences = self.contexts.getSampleSentences()
            if (self.contexts.getQuestionIndex() is not -1):
                if len(sentence) != 0:
                    ind = self.contexts.getQuestionIndex()
                    needed = self.contexts.getParamsNeeded()
                    found = self.contexts.getParamsFound()
                    value = self.contexts.getParamsValue()
                    lists = self.contexts.getQuestionList()
                    for i in range(0, len(needed)):
                        if needed[i]["name"] == lists[ind]["name"]:
                            value[i] = sentence
                            found[i] = True
                            break
                    self.contexts.setParamsValue(value)
                    self.contexts.setParamsFound(found)