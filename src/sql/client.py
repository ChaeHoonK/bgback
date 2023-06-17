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
        self.cursor.close: bool
        self.connection.close()

    def commit(self):
        self.connection.commit()


