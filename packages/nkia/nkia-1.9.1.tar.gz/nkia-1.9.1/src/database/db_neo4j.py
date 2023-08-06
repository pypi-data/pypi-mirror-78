from neo4j import GraphDatabase

import database.db_credentials as db


class Neo4jDatabase(object):

    def __init__(self, environment):
        self.environment = environment
        self.neo4j_credentials = db.neo4j_credentials(environment)

    def connect(self):   
        complete_host = 'bolt://' + self.neo4j_credentials['host'] + ':' + str(self.neo4j_credentials['port'])

        driver = GraphDatabase.driver(complete_host, auth=(self.neo4j_credentials['user'], self.neo4j_credentials['passwd']))

        return driver

    def match(self, query, driver, params=None):
        with driver.session() as session:
            result = session.read_transaction(self.execute_query, query, params)

        driver.close()
        
        return result

    def execute_query(self, tx, query, params):
        if params is not None:
            query_result = tx.run(query, params)
        else:
            query_result = tx.run(query)

        response = [result for result in query_result]

        return response
