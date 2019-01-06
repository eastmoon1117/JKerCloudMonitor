#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jwt, datetime, time
from flask import jsonify
from config import Config
from strings.AuthStrings import AuthStrings

class Auth:
    def __init__(self):
        pass

    @staticmethod
    def encode_auth_token(user_id, login_time):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=180, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                Config.TOKEN_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            payload = jwt.decode(
                auth_token, 
                Config.TOKEN_KEY, 
                options={'verify_exp': False}
            )
            if 'data' in payload and 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return AuthStrings.token_is_expired
        except jwt.InvalidTokenError:
            return AuthStrings.token_is_invalid
    
    @staticmethod
    def encode_app_token(app_key, app_secret):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=180, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'app_key': app_key,
                    'app_secret': app_secret
                }
            }
            return jwt.encode(
                payload,
                Config.TOKEN_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_app_token(auth_token):
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            payload = jwt.decode(
                auth_token, 
                Config.TOKEN_KEY, 
                options={'verify_exp': False}
            )
            if 'data' in payload and 'app_key' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return AuthStrings.token_is_expired
        except jwt.InvalidTokenError:
            return AuthStrings.token_is_invalid

