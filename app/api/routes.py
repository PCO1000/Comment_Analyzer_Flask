from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Text, text_schema, texts_schema
from dotenv import load_dotenv
import requests
import json
import os

api = Blueprint('api',__name__, url_prefix='/api')

load_dotenv()
API_KEY = os.getenv("API_KEY")

url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

@api.route('/getdata')
def getdata():
    return {'yee': 'naw'}

@api.route('/texts', methods = ['POST'])
@token_required
def create_text(current_user_token):
    comment = request.json['comment']
    user_token = current_user_token.token
    requested_attributes = {"TOXICITY": {}}

    
    data = {
        'comment': {"text": comment},
        'requestedAttributes': requested_attributes,
        'languages': ['en'],
    }

    

    params = {
        "key": API_KEY
    }

    try:
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()  # Raise exception for bad response status
        result = response.json()
        toxicity_score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        print("Toxicity score:", toxicity_score)

        text = Text(comment, str(toxicity_score), user_token=user_token)

        db.session.add(text)
        db.session.commit()

        response = text_schema.dump(text)
        return jsonify(response), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch toxicity score: {e}"}), 500


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
    requested_attributes = {"TOXICITY": {}}

    data = {
    "comment": {"text": text.comment},
    "requestedAttributes": requested_attributes,
    "languages": ["en"], 
    }

    params = {
        "key": API_KEY
    }

    try:
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()  # Raise exception for bad response status
        result = response.json()
        toxicity_score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        print("Toxicity score:", toxicity_score)
        text.toxicity_score = str(toxicity_score)

        db.session.commit()
        response = text_schema.dump(text)
        return jsonify(response), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch toxicity score: {e}"}), 500




    #response = requests.post(url, params=params, json=data)
    #result = response.json()
    #toxicity_score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    #print("Toxicity score:", toxicity_score)
    #text.toxicity_score = str(toxicity_score)

    #db.session.commit()
    #response = text_schema.dump(text)
    #return jsonify(response)


# DELETE car ENDPOINT
@api.route('/texts/<id>', methods = ['DELETE'])
@token_required
def delete_text(current_user_token, id):
    text = Text.query.get(id)
    db.session.delete(text)
    db.session.commit()
    response = text_schema.dump(text)
    return jsonify(response)


