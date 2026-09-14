#初期化処理

from flask import Flask
app = Flask(__name__)

import flaskr.main

from flaskr import db
db.create_events_table()