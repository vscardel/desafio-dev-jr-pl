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
	if graph:
		#graph[0] stores the id and graph[1] the json data
		json_string = json.loads(graph[1])
		payload = {'id':graph[0], 'data':json_string['data']}
		return jsonify(payload),200
	else:
		return Response("",status=404)
	conn.close()

@app.route('''/routes/<int:graph_id>/from/<string:town1>/to/<string:town2>''', methods = ['GET','POST'])
def find_all_routes(graph_id,town1,town2):
	maxStops = int(request.args.get("maxStops"))
	url_get_graph = "http://localhost:8080/graph/" + str(graph_id)
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	#response with graph
	response = requests.get(url_get_graph,headers=headers)
	if response.status_code == 404:
		#return 500 for testing purposes
		return Response("",status_code=500)
	#dict object
	json_response = response.json()
	graph = Graph(json_response)
	all_paths = graph.find_all_routes(town1,town2,maxStops)
	#generate the response payload
	payload = {"routes":[]}
	for path in all_paths:
		payload["routes"].append({
				"route":''.join(path),
				"stops":len(path)-1
		})
	return jsonify(payload),200

@app.route("/distance/<int:graph_id>/from/<string:town1>/to/<string:town2>")
def find_min_distance(graph_id,town1,town2):
	url_get_graph = "http://localhost:8080/graph/" + str(graph_id)
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	#response with graph
	response = requests.get(url_get_graph,headers=headers)
	if response.status_code == 404:
		#return 500 for testing purposes
		return Response("",status_code=500)
	#dict object
	json_response = response.json()
	graph = Graph(json_response)
	distance = graph.find_min_distance(town1,town2,maxStops)
	#generate the response payload
	payload = "dummy_payload"
	return jsonify(payload),200

if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True,port=8080)