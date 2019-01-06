#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import app
from flask import Flask, jsonify, request, abort
from datetime import datetime
from models.user import User
from models.device import Device
from auth import Auth

@app.route('/todo/api/v1/user', methods=['GET'])
def get_user():
    devices = Device.objects().all()
    print devices 
    
    user = User.objects(name="test2").first()
    print user
    
    #user.update(device=device)
    #user.update(devices=devices)
    #print device.devicename
    
    #user.update(emdevices=devices)
    print user.name
    token = Auth.encode_auth_token(2, 100000)
    print "token:" + token
    payload = Auth.decode_auth_token(token)
    print payload
    print payload['data']['id']
    
    return jsonify({'userinfo': User.objects.all()}), 201

@app.route('/todo/api/v1/user', methods=['POST'])
def create_user():
    if not request.json or not 'name' in request.json or not 'password' in request.json:
        print(request)
        abort(400)
    
    #user = User(name=request.json['name'], password=request.json['password']).save();
    return jsonify({'userinfo': User.objects.all()}), 201

