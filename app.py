from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://eoexzqqlqiqssi:4014e8028143ca279bbdd8a8c9e804479d63070d0a34ad7297c8e6415af68f7e@ec2-3-216-129-140.compute-1.amazonaws.com:5432/dbe76jpdh8ust4"

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

# Schema formats data
class CharacterSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'character_class', 'hitpoints')

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many = True)


@app.route('/character/add', methods = ['POST'])
def add_character():
    if request.content_type != 'application/json':
        return jsonify("Error: data must be sent as json")

    post_data = request.get_json()
    name = post_data.get('name')
    character_class = post_data.get('character_class')

    record = Character(name, character_class)
    db.session.add(record)
    db.session.commit()

    return jsonify('character created')

@app.route('/character/get', methods = ['GET'])
def get_all_characters():
    all_characters = db.session.query(Character).all()
    return jsonify(characters_schema.dump(all_characters))

@app.route('/character/get/<id>', methods = ['GET'])
def get_character_by_id(id):
    character = db.session.query(Character).filter(Character.id == id).first()
    return jsonify(character_schema.dump(character))

@app.route('/character/delete/<id>', methods =['DELETE'])
def delete_character_by_id(id):
    character = db.session.query(Character).filter(Character.id == id).first()
    db.session.delete(character)
    db.session.commit()
    return jsonify('character deleted')

if __name__ == "__main__":
    app.run(debug=True)