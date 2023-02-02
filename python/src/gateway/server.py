import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from .. import channel

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server) #abstracting handling of MongoDB connection
fs = gridfs.GridFS(mongo.db) #enable handling of files > 16MB

queue = channel.get_queue("VideoMP3Queue") # Get active AWS SQS Queue

@server.route("/login", methods=["POST"])
def login():  
  token, err = access.login(request)
  return token if not err else err

@server.route("/upload", methods=["POST"])
def upload():
	access, err = validate.token(request)
	access = json.loads(access)

	if access["admin"]:
		if len(request.files) != 1:
			return "Exactly 1 file required", 400 

		for _, f in request.files.items():
			err = util.upload(f, fs, queue, access)
			if err: 
				return err
		
		return "success", 200
	else:
		return "not authorized", 401

@server.route("/download", methods=["GET"])
def download():
	pass

if __name__ == "__main__":
	server.run(host="0.0.0.0", port=8080)

