import sys
from service import action
if '/Users/naveen-pt2724/project/common' not in sys.path:
    sys.path.insert(0, '/Users/naveen-pt2724/project/common')
print(sys.path)
import context
import exceptions
class nlp:
    con = None
    actions = None
    def __init__(self):
        self.con = context.Context()
    def getResponse(self,sentence):
        #self.con.setIsPresent(True)
        #print(self.con.getIsPresent())
        if(self.con.getIsPresent()==True):
            #print('go to paramsDetection')
            cv=context.Context()
            #print("ans="+str(cv.getIsPresent()))
            #print(self.con.getIsPresent())
        else:
            #print('go to ActionDetection')
            try:
                self.actions = action.ActionDetection()
                self.actions.findAction(sentence)
                #self.con.setIsPresent(True)
            except exceptions.InvalidApiKey:
                raise exceptions.InvalidApiKey("Invalid ApiKey found")
            except exceptions.ActionNotFound:
                raise exceptions.ActionNotFound("Action not Detected")
        cv=context.Context()
        #print("ans="+str(cv.getIsPresent()))
