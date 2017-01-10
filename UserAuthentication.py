from AppRepository import AppRepository
import uuid
import tornado.web
import datetime
import json

class UserAuthentication(tornado.web.RequestHandler):
    
    # To register new Apps
    @tornado.web.asynchronous
    def post(self):
        data = self.request.body
        provided = json.loads(data)
        if 'secret' not in provided:
            value = {'id':str(uuid.uuid4()).strip(), 'name':provided['name'], 'is_encrypted':False, 'secret':str(uuid.uuid4()).strip()}
            details = AppRepository().store(value)
            if details:
                self.set_header("Content-Type", "application/json")
                self.write(json.dumps(details))
            else:
                self.set_status(409)
                self.set_header("Content-Type", "application/json")
                self.write(json.dumps({'message':'Already Exists', 'error_code':409}))
                
        else:
            value = {'id':provided['id'], 'secret':provided['secret']}
            details = AppRepository().get_by_id(value)
            if details:
                self.set_header("Content-Type", "application/json")
                self.write(json.dumps(details))
            else:
                self.set_status(404)
                self.set_header("Content-Type", "application/json")
                self.write(json.dumps({'message':'App name not exists', 'error_code':404}))
        self.finish()

    def get(self):
        data = AppRepository().get_all()
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(data))