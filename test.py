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
		return response

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
		response_get_graph = self.test_save_graph_sucessfull_payload() 
		url = "http://localhost:8080/graph/"+str(response_get_graph.json()['id'])
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.get(url,headers=headers)
		self.assertEqual(response.status_code,200)

	#tests if the json graph is returned by retrieve_graph
	def test_retrieve_graph_returns_json_response(self):
		response_get_graph = self.test_save_graph_sucessfull_payload() 
		url = "http://localhost:8080/graph/"+str(response_get_graph.json()['id'])
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.get(url,headers=headers)
		self.assertTrue(response.json())

	#test if receive_graph returns 404 for non existing graph on db
	def test_retrive_graph_graph_dont_exists(self):
		url = "http://localhost:8080/graph/0"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.get(url,headers=headers)
		self.assertEqual(response.status_code,404)

	#tests if the payload have the id on it
	def test_retrive_graph_id_on_payload(self):
		response_get_graph = self.test_save_graph_sucessfull_payload() 
		url = "http://localhost:8080/graph/"+str(response_get_graph.json()['id'])
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.get(url,headers=headers)
		json_response = response.json()
		self.assertTrue(response.json()['id'])

	#tests if find_all_routes returns 404 for graph not found
	def test_find_all_routes_not_found(self):
		url = "http://localhost:8080/routes/0/from/A/to/B"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.post(url,headers=headers)
		self.assertEqual(response.status_code,500)

	#testing url with maxStops parameter
	def test_find_all_routes_not_found_with_maxStops(self):
		url = "http://localhost:8080/routes/0/from/A/to/B?maxStops=10"
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

	#test json response payload for graph on db
	def test_find_all_routes_response(self):
		url = "http://localhost:8080/routes/14/from/A/to/B?maxStops=10"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.post(url, headers=headers)
		self.assertEqual(response.json(),{'routes': 
				[{'route': 'AB', 'stops': 1}, 
				{'route': 'AEB', 'stops': 2}, 
				{'route': 'AEDB', 'stops': 3}]})

	#test json response payload for graph on db without maxStop
	def test_find_all_routes_response(self):
		response_get_graph = self.test_save_graph_sucessfull_payload() 
		url = "http://localhost:8080/routes/"+str(response_get_graph.json()['id'])+"/from/A/to/C"
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		response = requests.post(url, headers=headers)
		self.assertTrue(response.json())

	#tests return_graph_as_adjacency_matrix function
	def test_return_graph_as_adjacency_matrix(self):
		test_graph = graphs['test_graph_2']
		my_graph = Graph(test_graph)
		adjacency_matrix =  my_graph.return_graph_as_adjacency_matrix()
		self.assertEqual(adjacency_matrix,
			([[0, 5, 0, 5, 7], 
			[0, 0, 4, 0, 0], 
			[0, 0, 0, 8, 2], 
			[0, 0, 8, 0, 6], 
			[0, 3, 0, 0, 0]], 
			{'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}))

	#test find_min_distance function
	def test_min_distance(self):
		test_graph = graphs['test_graph_1']
		my_graph = Graph(test_graph)
		adjacency_matrix =  my_graph.return_graph_as_adjacency_matrix()
		min_dist = my_graph.find_min_distance("A","C")
		self.assertEqual(min_dist,8)

	#test find_min_distance_with_path function
	def test_min_distance_with_path(self):
		test_graph = graphs['test_graph_1']
		my_graph = Graph(test_graph)
		min_path,min_distance = my_graph.find_min_distance_with_path("A","C")
		self.assertEqual((min_path,min_distance),(['A','B','C'],8))

	#test find_min_distance with a json request to a saved graph
	def test_request_min_distance(self):
		url = "http://localhost:8080/routes/14/from/A/to/C"
		test_graph = graphs['test_graph_1']
		my_graph = Graph(test_graph)
		min_path,min_distance = my_graph.find_min_distance_with_path("A","C")
		self.assertEqual((min_path,min_distance),(['A','B','C'],8))

if __name__ == '__main__':
	unittest.main()