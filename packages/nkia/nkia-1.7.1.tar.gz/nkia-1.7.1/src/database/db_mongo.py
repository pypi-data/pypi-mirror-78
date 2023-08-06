import pymongo
import sys
import ssl

import database.db_credentials as db

class MongoDatabase(object):

    def __init__(self, environment):
        self.environment = environment
        self.mongo_credentials = db.mongo_credentials(environment)

    def connect(self):
        self.conn = pymongo.MongoClient(
            self.mongo_credentials["uri"],
            ssl=self.mongo_credentials["ssl"],
            ssl_cert_reqs=ssl.CERT_NONE
        )

        self.db = self.conn['bi']
        sys.stdout.flush()

    def close_connection(self):
        self.conn.close()

        sys.stdout.flush()
    
