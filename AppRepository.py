from Repository import *
import tornado
import tornado.web

class AppRepository():
    def store(self, data):
        isAppExist = Repository().fetchDetailsWithoutJoin('Apps', {'name':data['name']})
        if isAppExist:
            return False
        newApp = Repository().store('apps', data)
        if newApp:
            return Repository().fetchDetailsWithoutJoin('apps', newApp)
        else:
            return False

    def get_all(self):
        return Repository().fetchDetailsWithoutJoin('apps')

    def get_by_id(self, data):
        return Repository().fetchDetailsWithoutJoin('apps', data)