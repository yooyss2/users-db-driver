from core import execute
from endpoint import route, request

from uuid import UUID

import json


clauses_fields = [
  "id",
  "firstname",
  "lastname",
  "username",
  "birthday",
  "joindate"
]

update_fields = [
  "firstname",
  "lastname",
  "username",
  "birthday"
]


@route("/select_customers", methods=("GET",))
def select_customers():
  
  try:
    if len(request.args.keys()) == 0:
      return json.dumps(execute("select_customers", (100, 0, None)))

    else:

      limit = 100
      offset = 0
      
      params = request.args.to_dict()

      if "offset" in params and "limit" not in params:
        return json.dumps({"400": "Bad Request"}), 400

      if "limit" in params:
        limit = int(params["limit"])
        if limit < 1:
          return json.dumps({"400": "Bad Request"}), 400
        if limit > 100:
          return json.dumps({"400": "Bad Request"}), 400
        del params["limit"]

        if "offset" in params:
          offset = int(params["offset"])
          if offset < 0:
            return json.dumps({"400": "Bad Request"}), 400
          del params["offset"]

      if len(params) > 0:

        if "id" in params:
          try:
            UUID(params["id"])
          except ValueError:
            return json.dumps({"400": "Bad Request"}), 400

        for field in params:
          if field not in clauses_fields:
            return json.dumps({"400": "Bad Request"}), 400

      return json.dumps(execute("select_customers", (limit, offset, params))), 200

  except Exception:
    return json.dumps({"500": "Internal Server Error"}), 500


@route("/update_customer", methods=("POST",))
def update_customer():
  
  try:

    if (len(request.form.keys()) > 0 and "id" in request.args.keys()):

      try:
        UUID(request.args.get("id"))
      except ValueError:
        return json.dumps({"400": "Bad Request"}), 400
      
      for field in request.form.keys():
        if field not in update_fields:
          return json.dumps({"400": "Bad Request"}), 400
      
      for clause in request.args.keys():
        if clause not in clauses_fields:
          return json.dumps({"400": "Bad Request"}), 400

      return json.dumps(execute("update_customer", (request.form.to_dict(), {"id": request.args.get("id")})))

    else:
      return json.dumps({"400": "Bad Request"}), 400
  
  except Exception:
    return json.dumps({"500": "Internal Server Error"}), 500
