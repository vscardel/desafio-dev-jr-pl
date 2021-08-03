from test_objects import graphs
import json
import requests
import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

	#test if the http response for sucessfully storing a graph
	#is 201
	def test_store_sucessfull_response_code(self):
		test_graph = graphs['test_graph_1']
		url = "http://localhost:8080/graph"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.post(url, 
			data=json.dumps(test_graph), 
			headers=headers)
		self.assertEqual(response.status_code,201)

	#check if the store payload returns the id
	def test_store_sucessful_payload(self):
		test_graph = graphs['test_graph_1']
		url = "http://localhost:8080/graph"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.post(url, 
			data=json.dumps(test_graph), 
			headers=headers)
		self.assertTrue(response.json()['id'])

	#tests if storing returns the code 400 for an empty graph
	def test_store_bad_request(self):
		test_graph = graphs['None']
		url = "http://localhost:8080/graph"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.post(url, 
			data=json.dumps(test_graph), 
			headers=headers)
		self.assertEqual(response.status_code,400)


if __name__ == '__main__':
	unittest.main()