import string
from nltk.corpus import stopwords
import constant
class preprocess:
    def preprocess(self,message):
        message=self.removePunctuation(message)
        message=self.removeStopwords(message)
        return message
    def removePunctuation(self,message):
         message_modified=""
         for char in message:
             if char not in string.punctuation:
                 message_modified=message_modified+char
         return message_modified
    def removeStopwords(self,message):
        constants=constant.constants()
        stopword=stopwords.words('english')
        message_split=message.split(' ')
        message_modified=[]
        for word in message_split:
            if word in stopword and word in constants.neglectStopwords:
                message_modified.append(word)
            elif word not in stopword:
                message_modified.append(word)
        return ' '.join(message_modified)
trial=preprocess()
print(trial.preprocess("tomorrow, is my birthday!! ,after that i am going to sleep:)"))
