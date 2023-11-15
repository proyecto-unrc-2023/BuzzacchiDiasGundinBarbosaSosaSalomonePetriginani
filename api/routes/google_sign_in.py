from flask import Flask, request, jsonify, session
from flask_restful import Resource, Api
from google.oauth2 import id_token
from google.auth.transport import requests
from api.routes import api

class GoogleSignIn(Resource):
    def post(self):
        try:
            # Verificar token id from client
            idinfo = id_token.verify_oauth2_token(request.json['id_token'], requests.Request(), "450042762936-gsjdaj4lh1ftmac3md1nvs1dufhbprgt.apps.googleusercontent.com")

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            email = idinfo['email']
            name = idinfo['name']

            session['username'] = name

            return jsonify({
                'correo': email,
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