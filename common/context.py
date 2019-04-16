import en_core_web_sm
import spacy
class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance
class Context(Singleton):
    SampleSentences = None
    actionDetected = None
    paramsNeeded = None
    paramsFound = None
    paramsValue = None
    isPresent = False
    instance = None
    paramsPosition = None
    apiKey = None
    questionIndex = -1
    questionList = None
    powerWords = [ "stop" , ""]
    nlpModel = spacy.load('en_core_web_sm')
    history = list()

    def getInstance(self):
        if self.instance is None:
            self.instance = Context()
            #self.nlpModel = spacy.load('en_core_web_sm')
            return self.instance
        return self.instance

    def getHistory(self):
        return self.history
    def getNlpModel(self):
        return self.nlpModel
    def getQuestionList(self):
        return self.questionList
    def getQuestionIndex(self):
        return self.questionIndex
    def getActionDetected(self):
        return self.actionDetected
    def getParamsNeeded(self):
        return self.paramsNeeded
    def getParamsFound(self):
        return self.paramsFound
    def getParamsValue(self):
        return self.paramsValue
    def getIsPresent(self):
        return self.isPresent
    def getApiKey(self):
        return self.apiKey
    def getSampleSentences(self):
        return self.SampleSentences
    def getParamsPosition(self):
        return self.paramsPosition
    def getPowerWords(self):
        return self.powerWords

    def setHistory(self,history):
        self.history=history
    def setQuestionList(self,questionList):
        self.questionList = questionList
    def setQuestionIndex(self,questionIndex):
        self.questionIndex = questionIndex
    def setParamsPosition(self,paramsPosition):
        self.paramsPosition=paramsPosition
    def setActionDetected(self,actionDetected):
        self.actionDetected = actionDetected
    def setParamsNeeded(self,paramsNeeded):
        self.paramsNeeded = paramsNeeded
    def setParamsFound(self,paramsFound):
        self.paramsFound = paramsFound
    def setParamsValue(self,paramsValue):
        self.paramsValue = paramsValue
    def setIsPresent(self,isPresent):
        self.isPresent = isPresent
    def setApiKey(self,apiKey):
        self.apiKey=apiKey
    def setSampleSentences(self,SampleSentences):
        self.SampleSentences=SampleSentences
