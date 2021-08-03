import io
import math
import csv
import requests
import pymysql
from app import app
from db import mysql
import json
from graph import Graph
from flask import Flask,request,Response

@app.route('/')
def index():
	return Response("Index", status=201)

@app.route('/graph',methods = ['GET','POST'])
def save_graph():
	conn = mysql.connect()
	cursor = conn.cursor()
	json_data = request.json
	conn.close()
	return Response(json_data, status=201)
	
if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True,port=8080)