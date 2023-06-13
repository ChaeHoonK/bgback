import math
from psycopg2 import connect, Error

from logic.logics import DBClient, Store

from sql.type import Store

def get_store_by_id(store_id):
    try:
        connection = connect(
            dbname="your_database",
            user="your_username",
            password="your_password",
            host="localhost"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT latitude, longitude FROM Stores WHERE storeUID = %s;", (store_id,))
        result:Store = cursor.fetchone()
        return (result.latitude, result.longitude)
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)

def haversine(lat1, lon1, lat2, lon2):
    radius = 6371  # radius of the earth in km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = radius * c
    return distance

def get_distance_by_id(storeA, storeB):
    lat1, lon1 = get_store_by_id(storeA)
    lat2, lon2 = get_store_by_id(storeB)
    distance = haversine(lat1, lon1, lat2, lon2)
    return int(distance)

def get_lan_lon(store:Store):
    return (store.latitude, store.longitude)

def get_distance(storeA, storeB):
    lat1, lon1 = get_lan_lon(storeA)
    lat2, lon2 = get_lan_lon(storeB)
    distance = haversine(lat1, lon1, lat2, lon2)
    return int(distance)
