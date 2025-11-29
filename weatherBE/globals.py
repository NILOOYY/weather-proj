# globals.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["weatherDB"]

# collections
users = db["users"]
weather_collection = db["weather"]
blacklist = db["blacklist"]   # used for logout / revoked tokens

# jwt secret
SECRET_KEY = "super_secret_weather_key"

