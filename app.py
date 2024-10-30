# pip install -r requirements.txt
from flask import Flask
from flask_graphql import GraphQLView
from database import db_session, init_db, connection_url


app = Flask(__name__)
app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = connection_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

with app.app_context():
    init_db()





