import requests
from test_objects import graphs
import json


if __name__ == '__main__':

	test_graph = graphs['test_graph_1']
	url = "http://localhost:8080/graph"
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	print('sending json')
	r = requests.post(url, data=json.dumps(test_graph), headers=headers)
	print(r.json())
	print('request sended')