import json

#class that represents a graph structure and
#its methods
class Graph():
	def __init__(self,json_dict):
		self.id = None
		self.structure = json_dict

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


	# def find_all_routes(self,town1,town2,maxStops):
	# 	graph = self.structure['data']
	# 	#tries to find the edge where town1 is the starting point