from collections.abc import Iterable
import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv
from typing import List



class Client:
    def __init__(self):
        load_dotenv()
        self.connection = psycopg2.connect(
            host=os.environ["DB_HOST"],
            dbname=os.environ['DATABASE'],
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD']
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def commit(self):
        self.connection.commit()
    
    def execute(self, query:str, data=None):
        self.cursor.execute(query, data)

    def query(self, query, data, fetch_one=True):
        self.cursor.execute(query, data)
        # Check if it's an INSERT query
        if 'INSERT' in query:
            # If so, fetch the result
            if fetch_one:
                result = self.cursor.fetchone()
            else:
                result = self.cursor.fetchall()
            return result
        else:
            return self.cursor.rowcount  # return number of affected rows



class ClientConnector:
    def __init__(self,):
        self.client = Client()
    
    def __enter__(self):
        return self.client

    def __exit__(self,*args):
        self.client.commit()
        self.client.close()

        