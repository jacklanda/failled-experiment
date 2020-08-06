# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
import pymongo

def client():
    return pymongo.MongoClient()

def create(db_name, col_name):
    db_ = client[db_name]
    col_ = db_[col_name]
    return col_

def insert(obj, col):
    col.insert_one(obj)

def delete(col):
    col.drop()

