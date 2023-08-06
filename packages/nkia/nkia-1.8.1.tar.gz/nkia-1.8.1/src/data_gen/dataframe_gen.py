
from datetime import datetime
import sys
import os 
from sys import argv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import json
import pymongo
import pandas as pd
import numpy as np

from database.db_mongo import MongoDatabase
from database.db_neo4j import Neo4jDatabase

class dataframeGen(object):

    def __init__(self, environment):
        self.environment = environment
        self.create_dataframe()
    
    def create_dataframe(self):
        self.open_database_connections()

        products_categories = self.get_products_categories()
        food_df = self.get_food_products_df(products_categories)

        not_food_df = self.get_not_food_products_df()
        food_and_not_food_df = self.concat_products_df(food_df.copy(), not_food_df.copy())

        self.save_dataframe(food_df, 'food_df')
        self.save_dataframe(food_and_not_food_df, 'food_and_not_food_df')

        self.close_mongo_connection()

    def open_database_connections(self):
        self.mongo = MongoDatabase(self.environment)
        self.mongo.connect()
        self.mongo_conn = self.mongo

        self.neo4j = Neo4jDatabase(self.environment)
        self.neo4j_conn = self.neo4j.connect()

    def get_products_categories(self):
        query = ''' MATCH (c:Category) WHERE c.name <> "categoria desconhecida" RETURN c '''
        products_categories = self.neo4j.match(query, self.neo4j_conn)

        return products_categories

    def get_food_products_df(self, products_categories):
        df_products = pd.DataFrame()

        query = ('''MATCH (p:Product)-[:FROM_CATEGORY]-(c:Category {name: $name})
           OPTIONAL MATCH (i:Ingredient)<-[:HAS_INGREDIENT]-(p)
                   RETURN p as product, i as ingredient, c as category''')

        for category in products_categories:
            products_from_category = self.neo4j.match(
                query, self.neo4j_conn, {'name': category[0]['name']})

            products_and_ingredients = self.create_products_dict(
                products_from_category)

            category_dataframe = self.create_product_dataframe(
                products_and_ingredients)

            category_dataframe['Category'] = category[0]['name']

            df_products = pd.concat([df_products, category_dataframe], sort=True)

            print('Finished Category: ', category[0]['name'])
            sys.stdout.flush()
        return df_products

    def create_products_dict(self, products_and_ingredients):
        products_and_ingredients_dict = {}

        for record in products_and_ingredients:
            product_name = record['product']['name']

            product_ingredient = record.get(
                'ingredient') if record.get('ingredient') != None else {}

            product_ingredient = product_ingredient.get(
                'name') if product_ingredient != {} else ''

            if product_name in products_and_ingredients_dict:
                products_and_ingredients_dict[product_name].append(
                    product_ingredient)
            else:
                products_and_ingredients_dict[product_name] = [
                    record['product'], product_ingredient]

        return products_and_ingredients_dict

    def create_product_dataframe(self, data):
        df_data = []

        for product in data.values():
            products_data = {}
            products_data = product[0]._properties
            products_data['ingredients'] = product[1:len(product)]
            df_data.append(products_data)

        return pd.DataFrame(df_data)

    def get_not_food_products_df(self):
        query = """MATCH (p:Product {is_food: false}) return p"""
        not_food_products = self.neo4j.match(query, self.neo4j_conn)
        not_food_product_dict = [x[0]._properties for x in not_food_products]

        return pd.DataFrame(data=not_food_product_dict)
 
    def concat_products_df(self, food_df, not_food_df):
        food_df['Category'] = 'food'
        not_food_df['Category'] = 'not food'

        return pd.concat([food_df.copy(), not_food_df.copy()], sort=True)

    def save_dataframe(self, dataframe, df_name):
        created = pd.datetime.now()

        for _, df in dataframe.groupby(np.arange(len(dataframe)) // 10000):

            payload = json.loads(df.to_json(orient='records'))
            
            self.mongo_conn.db[df_name].insert_one({
                'df': payload,
                'created': created
            })

    def close_mongo_connection(self):
        self.mongo.close_connection()
        
dataframeGen(argv[1] if len(argv) > 1 else 'dev')
