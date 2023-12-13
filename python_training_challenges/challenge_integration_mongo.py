"""
    Customer and Accounts on Mongo
"""
import pprint
from pymongo import MongoClient


#  Connect to MongoDB
client = MongoClient("mongodb+srv://corbaniedson:root@cluster0.bj7for7.mongodb.net/"
                     "?retryWrites=true&w=majority")
db = client.bank_database

#  Customer and Account collections
customers_collection = db.customers
accounts_collection = db.accounts

#  Insert customer data
customers_data = [
    {
        "name": "edson",
        "register_number": "07070707077",
        "address": "St, 156 - bla bla bla",
        "accounts": [
            {"type": "Individual", "agency": "0001", "account_number": 1, "balance": 0.0},
            {"type": "Individual", "agency": "0001", "account_number": 2, "balance": 100.00},
        ],
    },
    {
        "name": "joao",
        "register_number": "07070707055",
        "address": "St, 99 - bla bla bla",
        "accounts": [
            {"type": "Individual", "agency": "0001", "account_number": 3, "balance": 0.0},
        ],
    },
]

# Insert data into MongoDB
customers_collection.insert_many(customers_data)

# Query and display customer data
print("\nReturn users by a filter condition.")
filtered_customers = customers_collection.find({"name": {"$in": ["edson", "joao"]}})
for customer in filtered_customers:
    pprint.pprint(customer)

# Query and display account data
print("\nReturn Accounts.")
all_accounts = accounts_collection.find({"customer_id": {"$exists": True}})
for account in all_accounts:
    pprint.pprint(account)
