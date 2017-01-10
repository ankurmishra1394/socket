import json,os,uuid
import pymongo
import psycopg2

## Connect to database using psycopg2
connect = psycopg2.connect(database="sesocket", user="postgres", password="postgres", host="127.0.0.1", port="5432")

class MongoConnections:
    def __init__(self):     
        mongo = pymongo.MongoClient("localhost", 27017)
        self.db = mongo['server']
        self.collection = self.db['ClientMsg']
    def Collection(self):
        return self.collection

