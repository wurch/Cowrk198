from flask import Flask
import json
from pymongo import MongoClient

app = Flask(__name__)

with open('instance/config.json') as f:
    SECRET = json.load(f)

app.secret_key = SECRET['SECRET_KEY']
client = MongoClient(SECRET['MONGO_KEY'])
db = client['cwork-spendings']

import cwork.views