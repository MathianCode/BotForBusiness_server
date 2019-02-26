# import the nessecary pieces from Flask
from flask import Flask,render_template, request,jsonify,Response
from service import utils
#Create the app object that will route our calls
app = Flask(__name__)

@app.route('/test', methods = ['GET'])
def home():

#When run from command line, start the server
if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 3333, debug = True)
