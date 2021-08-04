from test_objects import graphs
import json
import requests
import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

	#test if the http response for sucessfully storing a graph
	#is 201
	def test_save_graph_sucessfull_response_code(self):
		test_graph = graphs['test_graph_1']
		url = "http://localhost:8080/graph"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.post(url, 
			data=json.dumps(test_graph), 
			headers=headers)
		self.assertEqual(response.status_code,201)

	#check if the store payload returns the id
	def test_save_graph_sucessfull_payload(self):
		test_graph = graphs['test_graph_1']
		url = "http://localhost:8080/graph"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.post(url, 
			data=json.dumps(test_graph), 
			headers=headers)
		self.assertTrue(response.json()['id'])

	#tests if storing returns the code 400 for an empty graph
	def test_save_graph_bad_request(self):
		test_graph = graphs['None']
		url = "http://localhost:8080/graph"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.post(url, 
			data=json.dumps(test_graph), 
			headers=headers)
		self.assertEqual(response.status_code,400)

	#test if the response code for an existing graph is 200
	def test_retrieve_graph_sucessfull_response_code(self):
		url = "http://localhost:8080/graph/14"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.get(url,headers=headers)
		self.assertEqual(response.status_code,200)

	#tests if the json graph is returned by retrieve_graph
	def test_retrieve_graph_returns_json_response(self):
		url = "http://localhost:8080/graph/14"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.get(url,headers=headers)
		self.assertTrue(response.json())

	#test if receive_graph returns 404 for non existing graph on db
	def test_retrive_graph_graph_dont_exists(self):
		#id -1 cannot exist on db
		url = "http://localhost:8080/graph/-1"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.get(url,headers=headers)
		self.assertEqual(response.status_code,404)


if __name__ == '__main__':
	unittest.main()