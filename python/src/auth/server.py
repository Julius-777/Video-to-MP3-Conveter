import jwt, datetime, os #set authentication expiration date and us os to set environment variables
from flask import Flask, request #Create our Server
from flask_mysqldb import MySQL #query MSQL database

server =Flask(__name__)
mysql = MySQL(server)

#config database credentials to allow us to connect to mysql db
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
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"))
    else:
        # User does not eexit
        return "invalid credentials", 401

@server.route("/validate", method=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
         return "missing credentials", 401
        
    encoded_jwt = encoded_jwt.split(" "[1])

    try:
        decoded =  jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithm=["HS256"]
        )
    except:
        return "not authorized", 403

    return decoded, 200

# Post user authetication and return JWT which user can use to make requests
# to the API
def createJWT(username, secret, authz):
      return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
        },
        secret,
        algorithm="HS256"
      )

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)  