from flask import request,jsonify
from controller.myController import myController
def init_routes(app):


    @app.before_request
    def before_request():
        print("Calling",request.endpoint)
        if request.endpoint != "login" and request.endpoint != "register":
            return myController.middleware()

    @app.route("/user/register",methods=["POST"])
    def register():
        return myController.register()
    
    @app.route("/user/login",methods=["POST"])
    def login():
        return myController.login()

    @app.route("/",methods=['GET'])
    def ping():
        return myController.ping()
    
    @app.route("/fetch",methods=['GET'])
    def fetch():
        return myController.fetch()
    

    @app.route("/",methods=['POST'])
    def addTodo():
        return myController.add()
    
    @app.route("/",methods=['DELETE'])
    def deleteTodo():
        return myController.delete()
    
    @app.route("/complete",methods=['POST'])
    def compleTodo():
        return myController.complete()
    


    
   
