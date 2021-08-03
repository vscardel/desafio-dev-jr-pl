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

#default page for localhost:8080
@app.route('/')
def index():
	return Response("Index", status=201)

#saves a graph on the database
@app.route('/graph',methods = ['GET','POST'])
def save_graph():
	conn = mysql.connect()
	cursor = conn.cursor()
	#python dict
	json_data = request.json
	if json_data:
		#format that can be inserted on mysql database
		json_string = json.dumps(json_data)
		insert_query = "INSERT INTO Graphs (graph) VALUES(%s)"
		try:
			cursor.execute(insert_query,json_string)
			new_id = cursor.lastrowid
			conn.commit()
			#payload
			return Response("",status=201)
		except:
			#http server error
			return Response("", status=500)
	conn.close()
	#if not json returns bad request code
	return Response(json_data, status=400)

if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True,port=8080)