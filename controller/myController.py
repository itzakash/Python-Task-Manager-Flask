from flask import jsonify,request,make_response
from pydantic import BaseModel,EmailStr,ValidationError,Field
import uuid
import bcrypt
import copy
import jwt

class UsersSchema(BaseModel):
    email : EmailStr
    password : str
    first_name : str
    last_name : str

class UserLoginSchema(BaseModel):
    email : EmailStr
    password : str

class TodoSchema(BaseModel):
    title : str


class MyController:
    def __init__(self):
        self.jwt_secret = "akash_todo"
        self.todo = [
        #     {
        #     "_id"  :1,
        #     "title" : "Learn Javascript",
        #     "isCompleted" : False
        # }
        ]
        self.users = [
            # {
            #     "_id" : 1,
            #     "email" : "skytalawar@gmail.com",
            #     "first_name" : "Akash",
            #     "last_name" : "Talawar",
            #     "password" : "73yr23yr872yr928r"
            # }
        ] # type: ignore


    def ping(self):
        return "PING"
    
    def fetch(self):
        todos = [todo for todo in self.todo if todo['_user_id'] == request.user_data['_id']]
        return jsonify(todos)
    
    def add(self):
        try:
            todo = TodoSchema(**request.json)
            item = todo.model_dump()
        except ValidationError as e: # return all validation error
            return jsonify(e.errors()), 400
        
        # item = request.json
        id = str(uuid.uuid4()) #generate random uuid 
        # if len(self.todo) > 1:
        #     id = self.todo[-1]["_id"]

        checkExist = [todo for todo in self.todo if todo['title'] == item['title'] and todo['_user_id'] == request.user_data['_id']]

        # print(len(checkExist))
        if len(checkExist) > 0:
            return jsonify(msg="Todo already exists!")
        
        item['isCompleted'] = False
        item['_id'] = id
        item['_user_id'] = request.user_data['_id']
        self.todo.append(item)
        return jsonify(item)
    
    def delete(self):
        todo_id = request.json['_id']

        index = next((index for index, obj in enumerate(self.todo) if obj['_id'] == todo_id),None)

        if index is not None:
            if self.todo[index]['isCompleted'] == False:
                return jsonify(msg='Todo is not completed Yet!.. Please complete it')
            else:
                del self.todo[index]
                return jsonify(msg = 'successfully deleted!'),200
        else:
            return jsonify(msg='Todo not found'),404

    def complete(self):
        todo_id = request.json['_id']

        index = next((index for index, obj in enumerate(self.todo) if obj['_id'] == todo_id),None)

        if index is not None:
            if self.todo[index]['isCompleted'] == True:
                return jsonify(msg='Todo Already completed in list')
            else:
                self.todo[index]['isCompleted'] = True
            
            return jsonify(msg='Todo marked completed...')
        else:
            return jsonify(msg='Todo not found'),404
        
    def register(self):

        # payload validation
        try:
            user = UsersSchema(**request.json)
            user_dict = user.model_dump()
        except ValidationError as e: # return all validation error
            return jsonify(e.errors()), 400
        
        try:
            exits = self.checkExist(self.users,"email",user_dict['email'])

            if exits is None:
                user_dict["_id"] = str(uuid.uuid4()) #generate random uuid 
                user_dict["password"] = self.hashPassword(user_dict['password'])
                self.users.append(user_dict)
                return jsonify(msg="User register successfully",user=user_dict)
            else:
                return jsonify(msg="User already registered..."),409
        except Exception as e: 
            print(e)
            return jsonify({"error" :  f"An unexpected error occurred: {str(e)}"}),500
    
    def login(self):
        try:
            payload = UserLoginSchema(**request.json)
            payload_dict = payload.model_dump()
        except ValidationError as e:
            return jsonify(e.errors()),400
        
        user = [user for user in self.users if user['email'] == payload_dict['email']]

        if len(user) > 0:
            # print(user)
            userPassword =  payload_dict['password']
            user = copy.deepcopy(user[0]) #avoid references

            
            result : bool = self.verifyPassword(userPassword,user['password']) 

            if result:
                del user['password']
                # print(self.users)
                token = self.generateToken(user)
                response = make_response(jsonify(msg="Login successful"))
                response.headers['Authorization'] = f'Bearer {token}'
                return response, 200
            else:
                return jsonify(msg="Invalid password") , 401

        else:
            return jsonify(msg = "Invalid User"), 401
        


    def checkExist(self,array,key,value)->any:
        index = next((index for index, obj in enumerate(array) if obj[key] == value),None)
        return index
    
    def generateToken(self,payload : dict) ->str:
        # payload['exp'] = 
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def hashPassword(self,password : str) ->str:
        # converting password to array of bytes 
        bytes = password.encode('utf-8') 
        
        # generating the salt 
        salt = bcrypt.gensalt()
        
        # Hashing the password 
        hash = bcrypt.hashpw(bytes, salt).decode('utf-8')
        return hash
    

    def verifyPassword(self,password:str,hashPassword :str)->bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashPassword.encode('utf-8')) 
    
    def middleware(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Unauthorized"}),401
        
        token = auth_header.split(" ")[1]

        user_data = self.decode_token(token)

        if not user_data['_id']:
            return jsonify({"error": "Unauthorized"}), 401
        
        request.user_data = user_data

    def decode_token(self,token:str)->any:
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None






    

myController = MyController()