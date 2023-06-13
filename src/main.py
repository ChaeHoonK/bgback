from fastapi import FastAPI
import psycopg2
import socketio

sio = socketio.AsyncServer(async_mode='asgi')

DB_HOST = "localhost"
DB_NAME = "mydatabase"
DB_USER = "username"
DB_PASS = "password"


app = FastAPI()
app.mount('/', socketio.ASGIApp(sio))


@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


@app.get("/users/")
def read_users():
    # Connect to the database
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

    # Open a cursor to performello transactions
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        results = cur.fetchall()

    # Close the connection
    conn.close()

    return results

