from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Text, text_schema, texts_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'naw'}

@api.route('/texts', methods = ['POST'])
@token_required
def create_text(current_user_token):
    comment = request.json['comment']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    text = Text(comment, user_token = user_token )

    db.session.add(text)
    db.session.commit()

    response = text_schema.dump(text)
    return jsonify(response)

@api.route('/texts', methods = ['GET'])
@token_required
def get_text(current_user_token):
    a_user = current_user_token.token
    texts = Text.query.filter_by(user_token = a_user).all()
    response = texts_schema.dump(texts)
    return jsonify(response)


@api.route('/texts/<id>', methods = ['GET'])
@token_required
def get_single_text(current_user_token, id):
    text = Text.query.get(id)
    response = text_schema.dump(text)
    return jsonify(response)


# UPDATE endpoint
@api.route('/texts/<id>', methods = ['POST','PUT'])
@token_required
def update_text(current_user_token,id):
    text = Text.query.get(id) 
    text.comment = request.json['comment']
    text.user_token = current_user_token.token

    db.session.commit()
    response = text_schema.dump(text)
    return jsonify(response)


# DELETE car ENDPOINT
@api.route('/texts/<id>', methods = ['DELETE'])
@token_required
def delete_text(current_user_token, id):
    text = Text.query.get(id)
    db.session.delete(text)
    db.session.commit()
    response = text_schema.dump(text)
    return jsonify(response)


