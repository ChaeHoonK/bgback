'''CREATE TABLE Users (
    userUID UUID PRIMARY KEY,
    ID TEXT NOT NULL,
    PW TEXT NOT NULL,
    StoreUID UUID,
    PW2 TEXT,
    Phone TEXT,
    Wallet TEXT[]
);'''

'''CREATE TABLE Stores (
    storeUID UUID PRIMARY KEY,
    Phone TEXT,
    Name TEXT NOT NULL,
    Latitude NUMERIC,
    Longitude NUMERIC,
    Address TEXT,
    Menus TEXT,
    URLs TEXT
);'''

'''CREATE TABLE Items (
    itemUID UUID PRIMARY KEY,
    Name TEXT,
    Category1 TEXT,
    Category2 TEXT,
    Category3 TEXT
);
'''

'''CREATE TABLE Transactions (
    transactionUID UUID PRIMARY KEY,
    Timestamp TIMESTAMP,
    couponUID UUID,
    clientID UUID,
    hostID UUID
);
'''
