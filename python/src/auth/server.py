import jwt, datetime, os #authentication expiration date
from flask import Flask, request #Create our Server
from flask_mysqldb import MySQL #query MSQL database

server =Flask(__name__)
mysql = MySQL(server)

#config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization #provides is the credentials from a basic authorization header
    if not auth:
        # Invalid reqest missing details in header
        return "missing credentials", 401
        
# check db for username and password