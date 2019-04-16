import sys
import datetime
from service import action
if '/Users/naveen-pt2724/project/common' not in sys.path:
    sys.path.insert(0, '/Users/naveen-pt2724/project/common')
print(sys.path)
import errorCode
import context
import exceptions
import random
import server
import service
from service import ParamDetection
from service import NumberDetection
from service import StringDetection
class nlp:
    con = None
    actions = None
    def __init__(self):
        self.con = context.Context()

    def isparammissing(self):
        found = self.con.getParamsFound()
        for i in range(0,len(found)):
            if found[i] is False:
                return i
        return False
    def getCompletedResult(self):
        params = self.con.getParamsNeeded()
        paramsvalues = self.con.getParamsValue()
        values = list()
        for i in range(len(params)):
            obj = {}
            obj["paramname"] = params[i]["name"]
            obj["datatype"] = params[i]["datatype"]
            obj["value"] = paramsvalues[i]
            values.append(obj)
        return values

    def getHistory(self,sentence,rep):
        obj = {}
        obj["input"] = sentence
        obj["code"] = rep["code"]
        obj["date"] = datetime.datetime.now()
        obj["result"] = rep
        return obj

    def clearContext(self):
        self.con.setQuestionIndex(-1)
        self.con.setParamsNeeded(None)
        self.con.setParamsFound(None)
        self.con.setParamsValue(None)
        self.con.setQuestionList(None)
        self.con.setIsPresent(False)
        self.con.setActionDetected(None)
        self.con.setParamsPosition(None)
        self.con.setSampleSentences(None)
        self.con.setHistory(list())

    def getResponse(self,sentence):
        #self.con.setIsPresent(True)
        #print(self.con.getIsPresent())
        if len(sentence) == 0:
            resp = server.getresponsepojo("result", [errorCode.errors().BFB009, "BFB009"], ["message", "code"])
            his = self.con.getHistory()
            his.append(self.getHistory(sentence, resp))
            self.con.setHistory(his)
            return server.getresponse("result", [errorCode.errors().BFB009, "BFB009"], ["message", "code"])
        if sentence in self.con.getPowerWords():
            resp = server.getresponsepojo("result",[errorCode.errors().BFB010, "BFB010"],["message","code"])
            his = self.con.getHistory()
            his.append(self.getHistory(sentence, resp))
            self.con.setHistory(his)
            operation = server.getUserDBconnection()
            operation.update({"_id": self.con.getApiKey()}, {"$push": {"history": his}})
            self.clearContext()
            return server.getresponse("abort",[errorCode.errors().BFB010, "BFB010"],["message","code"])
        if(self.con.getIsPresent()==True):
            ind=self.con.getQuestionIndex()
            questions=self.con.getQuestionList()
            if questions[ind]["datatype"] == "Date":
                findParams = ParamDetection.paramDetection()
                findParams.DetectDates(sentence)
            if questions[ind]["datatype"] == "Number":
                findParams = NumberDetection.NumberDetection()
                findParams.detectNumber(sentence)
            if questions[ind]["datatype"] == "String":
                findParams = StringDetection.StringDetection()
                findParams.detectString(sentence)
            ind = self.con.getQuestionIndex()
            lists = self.con.getQuestionList()
            needed = self.con.getParamsNeeded()
            found = self.con.getParamsFound()
            for i in range(0, len(needed)):
                if needed[i]["name"] == lists[ind]["name"]:
                    if found[i] is True:
                        xxx = self.isparammissing()
                        if xxx is not False:
                            resp = server.getresponsepojo("result", [lists[ind+1]["question"], "BFB005",errorCode.errors().BFB005],
                                                      ["question", "code","message"])
                            his = self.con.getHistory()
                            his.append(self.getHistory(sentence,resp))
                            self.con.setHistory(his)
                            self.con.setQuestionIndex(self.con.getQuestionIndex()+1)
                            return server.getresponse("result", [lists[ind+1]["question"], "BFB005",errorCode.errors().BFB005],
                                                      ["question", "code","message"])
                        else:
                            final_action = self.con.getActionDetected()
                            final_params = self.getCompletedResult()
                            resp = server.getresponsepojo("result",
                                               [final_action, final_params, errorCode.errors().BFB006, "BFB006"],
                                               ["action", "value", "message", "code"])
                            his = self.con.getHistory()
                            his.append(self.getHistory(sentence, resp))
                            self.con.setHistory(his)
                            operation = server.getUserDBconnection()
                            operation.update({"_id": self.con.getApiKey()}, {"$push": {"history": his}})
                            print("history stored in DB..........")
                            self.clearContext()
                            return server.getresponse("result",
                                               [final_action, final_params, errorCode.errors().BFB006, "BFB006"],
                                               ["action", "value", "message", "code"])
                    else:
                        resp = server.getresponsepojo("result",["Sorry cannot understand :( ,"+lists[ind]["question"], "BFB005",errorCode.errors().BFB005],
                                                  ["question", "code","message"])
                        his = self.con.getHistory()
                        his.append(self.getHistory(sentence, resp))
                        self.con.setHistory(his)
                        return server.getresponse("result",["Sorry cannot understand :( ,"+lists[ind]["question"], "BFB005",errorCode.errors().BFB005],
                                                  ["question", "code","message"])
            #print("ans="+str(cv.getIsPresent()))
            #print(self.con.getIsPresent())
        else:
            #print('go to ActionDetection')
            try:
                self.actions = action.ActionDetection()
                self.actions.findAction(sentence)
                isfound = self.con.getParamsFound()
                paramname = self.con.getParamsNeeded()
                parammissing=list()
                RandomResponses = [""," Tell me about "," what about ","what is the "," Can i know the "]
                for i in range(0,len(isfound)):
                    if isfound[i] is False:
                        missing={}
                        missing["name"] = paramname[i]["name"]
                        missing["datatype"] = paramname[i]["datatype"]
                        missing["question"] = RandomResponses[random.randint(1,4)] + str(missing["name"]) + "?"
                        parammissing.append(missing)
                if len(parammissing)!=0:
                    self.con.setIsPresent(True)
                    self.con.setQuestionList(parammissing)
                    self.con.setQuestionIndex(0)
                    resp = server.getresponsepojo("result",[parammissing[0]["question"],"BFB005",errorCode.errors().BFB005],["question","code","message"])
                    his = self.con.getHistory()
                    his.append(self.getHistory(sentence, resp))
                    self.con.setHistory(his)
                    return server.getresponse("result",[parammissing[0]["question"],"BFB005",errorCode.errors().BFB005],["question","code","message"])
                else:
                    final_action = self.con.getActionDetected()
                    final_params = self.getCompletedResult()
                    resp = server.getresponsepojo("result",[final_action,final_params,errorCode.errors().BFB006, "BFB006"],["action","value","message", "code"])
                    his = self.con.getHistory()
                    his.append(self.getHistory(sentence, resp))
                    self.con.setHistory(his)
                    operation = server.getUserDBconnection()
                    operation.update({"_id": self.con.getApiKey()}, {"$push": {"history": his}})
                    self.clearContext()
                    return server.getresponse("result",[final_action,final_params,errorCode.errors().BFB006, "BFB006"],["action","value","message", "code"])
                #self.con.setIsPresent(True)
            except exceptions.InvalidApiKey:
                raise exceptions.InvalidApiKey("Invalid ApiKey found")
            except exceptions.ActionNotFound:
                raise exceptions.ActionNotFound("Action not Detected")
        cv=context.Context()
        #print("ans="+str(cv.getIsPresent()))
