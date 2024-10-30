# pip install -r requirements.txt
from flask import Flask
from flask_graphql import GraphQLView
from database import db_session, init_db


app = Flask(__name__)
app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://omermunk:1234@localhost:5432/ww2_operations'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


