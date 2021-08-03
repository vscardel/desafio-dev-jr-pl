import json

#class that represents a graph structure and
#its methods
class Graph():
	def __init__(self,json_dict):
		self.id = None
		self.structure = json_dict