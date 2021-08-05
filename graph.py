import json
from copy import copy

#class that represents a graph structure and
#its methods
class Graph():

	def __init__(self,json_dict):
		self.id = None
		self.structure = json_dict
		self.visited = {}

	#returns the json representation as a
	#dict: node->neighbours
	#ex: if A is a neighbour of E and D with distances 2 and 6
	#'A' -> [('E',2),('D',6)]
	def return_graph_as_dict_of_neighbours(self):
		#json structure
		dict_of_neighbours = {}
		original_representation = self.structure['data']
		for edge in original_representation:
			current_source = edge['source']
			#first time inserted
			if current_source not in dict_of_neighbours:
				dict_of_neighbours[current_source] = [(edge['target'],
												   edge['distance'])]
			else:
				dict_of_neighbours[current_source].append([(edge['target'],
												   edge['distance'])])
		return dict_of_neighbours

	#dfs for find_all_routes
	def dfs_find_all_routes(
		self,
		graph,
		curr_node,
		final_node,
		path,
		depht,maxStops):
		self.visited[curr_node] = True
		path.append(curr_node)
		depht += 1
		if curr_node == final_node:
			if len(path) <= maxStops + 1:
				#generate the answer
				yield copy(path)
		neighbours = graph[curr_node]
		for neighbour in neighbours:
			if neighbour[0][0] not in self.visited:
				yield from self.dfs_find_all_routes(
				graph,
				neighbour[0][0],
				final_node,path,depht,maxStops)
		path.pop()
		self.visited.pop(curr_node)
  

	def find_all_routes(self,town1,town2,maxStops):
		graph = self.return_graph_as_dict_of_neighbours()
		#dfs on graph to find all routes
		initial_stop = 0
		#list_with_path
		path = []
		all_paths = list(self.dfs_find_all_routes(
		graph,town1,town2,path,initial_stop,maxStops))
		return all_paths

	def flush(self):
		self.visited = {}