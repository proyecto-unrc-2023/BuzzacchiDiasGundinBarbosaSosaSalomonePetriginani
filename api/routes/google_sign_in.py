from flask import request, jsonify, session
from flask_restful import Resource
from google.oauth2 import id_token
from google.auth.transport import requests
from api.routes import api
from dotenv import load_dotenv
import os

load_dotenv()
class GoogleSignIn(Resource):
    def post(self):
        try:
            google_client_id = os.getenv('GOOGLE_CLIENT_ID')

            # Verify token id from client
            idinfo = id_token.verify_oauth2_token(request.json['id_token'], requests.Request(), google_client_id, clock_skew_in_seconds=10)

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            name = idinfo['name']
            session['username'] = name

            return jsonify({
                'success': True,
                'name': name
            })

        except ValueError:
            # Invalid token
            return jsonify({
                'msg': 'Error en la verificación del token',
                'error': 'Invalid token'
            })

api.add_resource(GoogleSignIn, '/google')