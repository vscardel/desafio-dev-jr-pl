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
				dict_of_neighbours[current_source].append((edge['target'],
												   edge['distance']))
		return dict_of_neighbours

	#returns the representation as a adjacency matrix
	#to map the original label of the vertex, the func-
	#tion also returns a dict "node->number".
	def return_graph_as_adjacency_matrix(self):
		original_representation = self.structure['data']
		vertex = {}
		#get all vertices first
		curr_num_vertice = 0
		for edge in original_representation:
			curr_vertice_1 = edge['source']
			curr_vertice_2 = edge['target']
			if curr_vertice_1 not in vertex:
				vertex[curr_vertice_1] = curr_num_vertice
				curr_num_vertice += 1
			if curr_vertice_2 not in vertex:
				vertex[curr_vertice_2] = curr_num_vertice
				curr_num_vertice += 1

		#matrix with initial distances set to 0
		adjacency_matrix = [[0 for column in range(len(vertex))]
			for row in range(len(vertex))]

		#second pass to update the adjacency matrix
		for edge in original_representation:
			curr_vertice_1 = edge['source']
			curr_vertice_2 = edge['target']
			position_i = vertex[curr_vertice_1]
			position_j = vertex[curr_vertice_2]
			adjacency_matrix[position_i][position_j] = edge['distance']

		return adjacency_matrix,vertex

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

	#find vertex that is not on sptSet and have
	#the minimum distance from curr_vertex
	def minDistance(self, dist, sptSet,vertex):
		min = float("inf")
		for v in range(len(vertex)):
			if dist[v] < min and sptSet[v] == False:
				min = dist[v]
				min_index = v
		return min_index

	def dijkstra(self,num_src,vertex,adjacency_matrix):
		#initial distances are +inf
		dist = [float('inf')] * len(vertex)
		#initial vertx distance is 0
		dist[num_src] = 0
		sptSet = [False] * len(vertex)
		for cout in range(len(vertex)):
			#vertex with minimun distance not yet
			#processed
			u = self.minDistance(dist, sptSet,vertex)
			#vertex now processed
			sptSet[u] = True
			#update the distances
			for v in range(len(vertex)):
				if adjacency_matrix[u][v] > 0 and sptSet[v] == False and \
				dist[v] > dist[u] + adjacency_matrix[u][v]:
					dist[v] = dist[u] + adjacency_matrix[u][v]
		return dist


	#uses dijikstra algorithm to find min route
	def find_min_distance(self,src,target):
		adjacency_matrix,vertex = self.return_graph_as_adjacency_matrix()
		num_src = vertex[src]
		dists = self.dijkstra(num_src,vertex,adjacency_matrix)
		return dists[vertex[target]]

	#find the path with min distance
	def find_min_distance_with_path(self,src,target):
		all_paths = self.find_all_routes(src,target,float("inf"))
		min_distance = self.find_min_distance(src,target)
		graph = self.return_graph_as_dict_of_neighbours()
		#determines if path is the min path
		min_path = None
		for path in all_paths:
			summ = 0
			for i in range(1,len(path)):
				source = path[i-1]
				target = path[i]
				for vertex in graph[source]:
					if vertex[0] == target:
						summ += vertex[1]
						break

			if summ == min_distance:
				min_path = path
		return min_path,min_distance

	def flush(self):
		self.visited = {}