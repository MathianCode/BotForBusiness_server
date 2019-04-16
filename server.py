# import the nessecary pieces from Flask
from flask import Flask,render_template, request,jsonify,Response,make_response
from bson import ObjectId
from pymongo import MongoClient
from preprocessing import constant
import hashlib
import time
import sys
import traceback
if '/Users/naveen-pt2724/project/common' not in sys.path:
    sys.path.insert(0, '/Users/naveen-pt2724/project/common')
import context
import exceptions
import errorCode
import random
from service import nlp
#from flask_cors import CORS,cross_origin
#from service import utils
#from preprocessing import preprocess
#Create the app object that will route our calls

#api's for the client frameworks


app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.sample #Select the database
todos = db.collection #Select the collection name
#CORS(app, resources={r"/api/v1/*": {"origins": "http://localhost:3000"}})
# abs=constant.constants()
# print(abs.neglectStopwords)

def isuserexist(username):
    operation=getUserDBconnection()
    result=operation.find({"username":username})
    for obj in result:
        if(obj["username"]==username):
            return True
    return False

def getUserDBconnection():
    database=client.BFB
    operation=database.user
    return operation

def getheaders(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods']= '*'
    resp.headers['Access-Control-Allow-Headers']= 'Content-Type'
    return resp

def getresponsepojo(pojo,messages,message_holders):
    response = {}
    for i in range(0, len(messages)):
        response[message_holders[i]] = messages[i]
    return response
def getresponse(pojo,messages,message_holders):
    result = {}
    result[pojo]=getresponsepojo(pojo,messages,message_holders)
    resp=make_response(jsonify(result))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/v1/login',methods=['OPTIONS'])
def login():
    df={"login":{"message":"success"}}
    resp = Response(df)
    return getheaders(resp)

@app.route('/api/v1/action',methods=['OPTIONS'])
def action():
    df={"login":{"message":"success"}}
    resp = Response(df)
    return getheaders(resp)

@app.route('/api/v1/signup',methods=['OPTIONS'])
def signup_option():
    df={"login":{"message":"success"}}
    resp = Response(df)
    return getheaders(resp)

@app.route('/api/v1/action/all',methods=['OPTIONS'])
def getAllActions_option():
    df={"login":{"message":"success"}}
    resp = Response(df)
    return getheaders(resp)

@app.route('/api/v1/signup',methods=['POST'])
def signup():
    data=request.get_json()
    if(isuserexist(data["signup"]["username"])):
        return getresponse("signup",["Username Exists","BFB002","-1"],["message","code","userid"])
    print(data)
    ticky=time.time()
    ss=str(ticky)+data["signup"]["username"]+data["signup"]["password"]
    hash_object = hashlib.md5(ss.encode())
    operation=getUserDBconnection()
    results=operation.insert({"_id":hash_object.hexdigest(),"username":data["signup"]["username"],"password":data["signup"]["password"]})
    print(results)
    print(hash_object.hexdigest())
    return getresponse("signup",["Signup Successfull!!",str(hash_object.hexdigest()),"BFB001"],["message","userid","code"])

@app.route('/api/v1/action',methods=['POST'])
def storeAction():
    data=request.get_json()
    print(data)
    operation=getUserDBconnection()
    action = data["action"]
    userid = data["action"]["userid"]
    action.pop('userid',None)
    operation.update({"_id" : userid },{ "$push" :{ "actions" : action}})
    return getresponse("action",["successfully stored",userid],["message","id"])

@app.route('/api/v1/action',methods=['GET'])
def getHistory():
    userid = request.args.get('userid')
    operation = getUserDBconnection()
    result = operation.find({"_id":userid})
    data = None
    for i in result:
        data = i
    if result.count() == 0:
        return getresponse("action",[errorCode.errors().BFB011,"BFB011"],["message","code"])
    return getresponse("action",[data,errorCode.errors().BFB001,userid],["user","message","id"])

@app.route('/api/v1/action/all',methods=['GET'])
def getAllActions():
    userid = request.args.get('userid')
    operation = getUserDBconnection()
    result = operation.find({"_id":userid})
    data = None
    for i in result:
        data = i
    if result.count() == 0 or "actions" not in data:
        return getresponse("action", [errorCode.errors().BFB011, "BFB011"], ["message", "code"])
    print(data["actions"])
    action_name = list()
    for act in data["actions"]:
        action_name.append(act["name"])
    return getresponse("action",[action_name,errorCode.errors().BFB001,userid],["actionNames","message","id"])

@app.route('/api/v1/login', methods = ['GET'])
def home():
    username = request.args.get('username')
    password = request.args.get('password')
    operation = getUserDBconnection()
    userid = -1
    result = operation.find({ "username" : username , "password" : password})
    if(result.count()==0):
        return getresponse("login",["Username or password combination is incorrect","BFB002","-1"],["message","code","userid"])
    else:
        for i in result:
            userid=i["_id"]
        return getresponse("login",["Login Successfull","BFB001",userid],["message","code","userid"])

@app.route('/api/v1/login',methods = ['POST','OPTIONS'])
#@cross_origin(origin='localhost')
def insert():
    data=request.get_json()
    print(data)
    #print(data["login"]["name"])
    cc=data["login"][0]
    cc["id"]="78"
    todos.insert(cc)
    resp=make_response(jsonify({"login":{"name":"naveen","id":"44"}}))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    #return jsonify({"name":"naveen","agge":str(type(x))});
    #todos.insert({"name":"happy","age":45})
    #return '<h1>'+"naveen kumar"+"</h1>";
    #sentence=request.args.get('sentence')




#NLP api's starts here -------------->

@app.route('/api/v1/BotForBusiness',methods = ['GET'])
def getResponse():
    sentence = request.args.get('sentence')
    apiKey = request.args.get('apikey')
    contexts=context.Context()
    contexts.setApiKey(apiKey)
    operations = nlp.nlp()
    try:
        return operations.getResponse(sentence)
    except exceptions.InvalidApiKey:
        return getresponse("error",[errorCode.errors().BFB008,"BFB008"],["message","code"])
    except exceptions.ActionNotFound:
        return getresponse("error",[errorCode.errors().BFB004,"BFB004"],["message","code"])
    except:
        operations.clearContext()
        traceback.print_exc()
        return getresponse("errror",[errorCode.errors().BFB007,"BFB007"],["message","code"])

if __name__ == '__main__':
    app.run(host ='localhost', port = 3333, debug = True)
