from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ""

db = SQLAlchemy(app)
ma = Marshmallow(app)

heroku = Heroku(app)
CORS(app)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    character_class = db.Column(db.String(), nullable = False)
    hitpoints = db.Column(db.Integer, nullable = False)

    def __init__(self, name, character_class):
        self.name = name
        self.character_class = character_class
        self.hitpoints = 100



if __name__ == "__main__":
    app.run(debug=True)