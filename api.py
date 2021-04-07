from flask import Flask
from flask_restful import Resource, Api, reqparse
import os

#TODO: add in actual database code
#TODO: assign api to actual Flask app
#TODO: figure out if we store datasets in database and if not, write code for sending zip file
#TODO: determine how to run this with javascript and if it works without flask having a front end portion
#TODO: add checkin function for hardware resources

app = Flask(__name__) # replace this with actual app
api = Api(app)
parser = reqparse.RequestParser()
db = getdb()


class HardwareResources(Resource):
    # get function that is called whenever we need to display the current hardware capacity for a hardware set
    def get(self, set_id):
        # get database information for that hardware set
        entry = db.get(set_id)
        if entry is not None:
            return entry
        return "Not found", 404

    # function for requesting hardware resources. called when someone sends request for checkout/checkin
    # checkout is a T/F variable for checkout and checkin respectively
    def post(self, set_id):
        parser.add_argument("checkout")
        parser.add_argument("amount")
        args = parser.parse_args()
        # get database information for that hardware set
        entry = db.get(set_id)
        if entry is not None:
            #set id is in the database, so we allow the checkout
            if args['checkout'] is "T":
                db.write(set_id, entry['capacity'] - int(args['amount']))
            #set id is in the database, so we allow the checkin
            else:
                db.write(set_id, entry['capacity'] + int(args['amount']))
            return entry, 200
        return "Not found", 404


class Projects(Resource):
    # get function that is called whenever we need to use an existing project for a user
    def get(self):
        parser.add_argument("project_id")
        args = parser.parse_args()
        # get database information for that project id
        entry = db.get(args['project_id'])
        if entry is not None:
            return entry
        return "Not found", 404

    # post function that is called whenever someone tries to create a new project
    def post(self):
        parser.add_argument("name")
        parser.add_argument("description")
        parser.add_argument("project_id")
        args = parser.parse_args()
        entry = db.get(args['project_id'])
        if entry is None:
            db.create(args['project_id'], args['name'], args['description'])
            return db.get(args['project_id']), 200
        return "Project id already exists" #plus some error code if needed


class Datasets(Resource):
    # get function that is called whenever someone requests to download dataset
    def get(self, dataset_id):
        entry = db.get(dataset_id)
        if entry is not None:
            # entry should be path to zip file?
            # send file code here if it is a file path
            # otherwise if database stores dataset directly, leave as is
            return entry
        return "Not found", 404


class Login(Resource):
    # get function that is called whenever someone is logging in
    def get(self, username, password):
        hashed_username = hash_function(username)
        hashed_password = hash_function(password)
        entry = db.get(hashed_username)
        if entry is not None and hashed_password is entry['password']:
            return username
        return "Incorrect username or password", 404

    # function is called whenever someone is registering
    def post(self, username, password):
        hashed_username = hash_function(username)
        hashed_password = hash_function(password)
        entry = db.get(username)
        if entry is None:
            db.create(hashed_username, hashed_password)
            return username, 200
        return "Username is already taken", #plus some error code if needed


api.add_resource(HardwareResources, '/HardwareResources/<set_id>')
api.add_resource(Projects, '/Projects/')
api.add_resource(Datasets, '/Datasets/<dataset_id>')
api.add_resource(Login, '/Login/<username>/<password>')



