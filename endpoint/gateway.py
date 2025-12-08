from .http import (
  request,
  Response,
  before_request,
  after_request
)

import json


sc_array = [
  "\"", "$",
  "&", "\'",
  "(", ")",
  "*", "+",
  ",", ";",
  "<", ">",
  "="
]


@before_request
def before_request():
  
  # if ("Authorization" not in request.headers or request.headers["Authorization"] != "Bearer "):

  #   response = Response("{\"401\": \"Unauthorized\"}")
  #   response.status = 401
  #   response.headers["WWW-Authenticate"] = "Bearer"

  #   return response

  params = request.args.to_dict()
  form = request.form.to_dict()

  if len(params) > 0:
    for param in params:
      if param == "" or params[param] == "":
        return json.dumps({"400": "Bad Request"}), 400

      for char in sc_array:
        if char in param or char in params[param]:
          return json.dumps({"400": "Bad Request"}), 400

  if len(form) > 0:
    for param in form:
      if param == "" or form[param] == "":
        return json.dumps({"400": "Bad Request"}), 400

      for char in sc_array:
        if char in param or char in form[param]:
          return json.dumps({"400": "Bad Request"}), 400
    

@after_request
def after_request(response):
  response.headers["Content-Type"] = "application/json"
  return response
