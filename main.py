import io
import math
import csv
import requests
import pymysql
from app import app
from db import mysql
import json
from graph import Graph
from flask import Flask,request,Response,jsonify

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
			json_data['id'] = new_id
			return jsonify(json_data),201
		except:
			#http server error
			return Response("", status=500)
	conn.close()
	#if not json returns bad request code
	return Response(json_data, status=400)

#retrieves a graph with id "graph_id from the database"
@app.route("/graph/<int:graph_id>")
def retrieve_graph(graph_id):
	conn = mysql.connect()
	cursor = conn.cursor()
	retrieve_query = "SELECT * FROM Graphs WHERE id = %s"
	try:
		cursor.execute(retrieve_query,str(graph_id))
	except:
		return Response("",status=500)
	graph = cursor.fetchone()
	#graph[0] stores the id and graph[1] the json data
	payload = {'id':graph[0], 'data':graph[1]}
	if graph:
		return jsonify(payload),200
	else:
		return Response("",status=404)
	conn.close()

if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True,port=8080)