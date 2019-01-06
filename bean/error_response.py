# -*- encoding: UTF-8 -*-

class ErrResponse(object):
    def __init__(self, code, error_code, message):
        self.code = code
        self.error_code = error_code
        self.message = message
 
