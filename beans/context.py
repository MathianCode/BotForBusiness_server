class context:
    contextName=str()
    paramName=list()
    paramValue=list()
    isContextSet=bool()
    contextID=int()
    def getContextName(self):
        return self.contextName
    def getParamName(self):
        return self.paramName
    def getParamValue(self):
        return self.paramValue
    def getIscontextSet(self):
        return self.isContextSet
    def getContextID(self):
        return self.contextID
    def setContextName(self,contextName):
        self.contextName=contextName
    def setParamName(self,paramName):
        self.paramName=paramName
    def setParamValue(self,paramValue):
        self.paramValue=paramValue
    def setIscontextSet(self,isContextSet):
        self.isContextSet=isContextSet
    def setContextID(self,contextID):
        self.contextID=contextID
