import requests
import json


if __name__ == '__main__':

	json_data = {
		"data":[
			{
			"source": "A", "target": "B", "distance": 6
			},
			{
			"source": "A", "target": "E", "distance": 4
			},
			{
		      "source": "B", "target": "A", "distance": 6
			},
		    {
		      "source": "B", "target": "C", "distance": 2
		    }
		    ,
		    {
		      "source": "B", "target": "D", "distance": 4
		    }
		    ,
		    {
		      "source": "C", "target": "B", "distance": 3
		    }
		    ,
		    {
		      "source": "C", "target": "D", "distance": 1
		    }
		    ,
		    {
		      "source": "C", "target": "E", "distance": 7
		    }
		    ,
		    {
		      "source": "D", "target": "B", "distance": 8
		    }
		    ,
		    {
		      "source": "E", "target": "B", "distance": 5
		    }
		    ,
		    {
		      "source": "E", "target": "D", "distance": 7
		    }
		    
		]
	}

	url = "http://localhost:8080/graph"
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	print('sending json')
	r = requests.post(url, data=json.dumps(json_data), headers=headers)
	print('request sended')