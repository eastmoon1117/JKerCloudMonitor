# -*- encoding: UTF-8 -*-

class AuthResponse(object):
    def __init__(self, token, refresh_token):
        self.refresh_token = refresh_token
        self.token = token

