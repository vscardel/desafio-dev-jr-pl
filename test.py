from test_objects import graphs
from graph import Graph
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
		url = "http://localhost:8080/graph/453"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.get(url,headers=headers)
		self.assertEqual(response.status_code,404)

	#tests if the payload have the id on it
	def test_retrive_graph_id_on_payload(self):
		url = "http://localhost:8080/graph/14"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.get(url,headers=headers)
		json_response = response.json()
		self.assertTrue(response.json()['id'])

	#tests if find_all_routes returns 404 for graph not found
	def test_find_all_routes_not_found(self):
		url = "http://localhost:8080/routes/453/from/A/to/B"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.post(url,headers=headers)
		self.assertEqual(response.status_code,500)

	#testing url with maxStops parameter
	def test_find_all_routes_not_found_with_maxStops(self):
		url = "http://localhost:8080/routes/453/from/A/to/B?maxStops=10"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.post(url,headers=headers)
		self.assertEqual(response.status_code,500)

	#tests return_graph_as_dict_of_neighbours() method on Graph	
	def test_return_graph_as_dict_of_neighbours(self):
		test_graph = graphs['test_graph_2']
		my_graph = Graph(test_graph)
		list_of_neighbours = my_graph.return_graph_as_dict_of_neighbours()
		self.assertTrue(list_of_neighbours)

	#test response for test_graph_2
	def test_find_all_routes_response(self):
		test_graph = graphs['test_graph_2']
		my_graph = Graph(test_graph)
		all_routes = my_graph.find_all_routes("A","C",3)
		my_graph.flush()
		self.assertEqual(all_routes,
						[['A', 'B', 'C'], 
						['A', 'D', 'C'], 
						['A', 'E', 'B', 'C']])

if __name__ == '__main__':
	unittest.main()