#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_mongoengine import MongoEngine
from config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MONGODB_SETTINGS'] = {
    'db':   Config.DB,
    'host': Config.Host,
    'port': Config.Port
}

# app.config.from_pyfile('config.json')
db = MongoEngine(app)

# 数据库对应的模型
# import models

# api的业务逻辑
import controllers

