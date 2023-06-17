'''CREATE TABLE Users (
    userUID SERIAL PRIMARY KEY,
    ID TEXT NOT NULL,
    PW TEXT NOT NULL,
    StoreUID INT,
    PW2 TEXT,
    Phone TEXT,
    Wallet TEXT[]
);'''

'''CREATE TABLE Stores (
    storeUID SERIAL PRIMARY KEY,
    Phone TEXT,
    Name TEXT NOT NULL,
    Latitude NUMERIC,
    Longitude NUMERIC,
    Address TEXT,
    Menus TEXT,
    URLs TEXT
);'''

'''CREATE TABLE Items (
    itemUID SERIAL PRIMARY KEY,
    Name TEXT,
    Category1 TEXT,
    Category2 TEXT,
    Category3 TEXT
);
'''

'''CREATE TABLE Transactions (
    transactionUID SERIAL PRIMARY KEY,
    Timestamp TIMESTAMP,
    couponUID UUID,
    clientID UUID,
    hostID UUID
);
'''
