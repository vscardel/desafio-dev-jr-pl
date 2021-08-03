import io
import math
import csv
import pymysql
from app import app
from db import mysql


@app.route('/')
def index():
	return("Hello World")

if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True,port=8080)