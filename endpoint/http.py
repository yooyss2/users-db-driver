import flask

server = flask.Flask(__name__)

route = server.route

request = flask.request
Response = flask.Response

before_request = server.before_request
after_request = server.after_request
