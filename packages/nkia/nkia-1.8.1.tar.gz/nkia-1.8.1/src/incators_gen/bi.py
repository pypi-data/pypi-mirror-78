
import sys
import os 
from sys import argv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.db_mongo import MongoDatabase
from database.db_neo4j import Neo4jDatabase
import utils.utils as utils


class BI(object):

    def __init__(self, environment):
        self.environment = environment
        self.utils = utils
        self.process_bi()

    def process_bi(self):
        self.open_database_connections()

        self.products_df = self.utils.get_dataframe_from_mongo(self.mongo_conn, 'food_df')

        self.close_mongo_connection()

    def open_database_connections(self):
        self.mongo = MongoDatabase(self.environment)
        self.mongo.connect()
        self.mongo_conn = self.mongo

        self.neo4j = Neo4jDatabase(self.environment)
        self.neo4j_conn = self.neo4j.connect()

    def close_mongo_connection(self):
        self.mongo.close_connection()

BI(argv[1] if len(argv) > 1 else 'dev')