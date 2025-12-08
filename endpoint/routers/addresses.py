from core import execute
from endpoint import route, request

from uuid import UUID

import json


clauses_fields = [
  "customer_id",
  "addresse_line_1",
  "addresse_line_2",
  "city",
  "country",
  "postal_code"
]


@route("/select_addresses", methods=("GET",))
def select_addresses():
  
  try:
    if len(request.args.keys()) == 0:
      return json.dumps(execute("select_addresses", (100, 0, None)))

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

        if "customer_id" in params:
          try:
            UUID(params["customer_id"])
          except ValueError:
            return json.dumps({"400": "Bad Request"}), 400

        for field in params:
          if field not in clauses_fields:
            return json.dumps({"400": "Bad Request"}), 400

      return json.dumps(execute("select_addresses", (limit, offset, params))), 200

  except Exception:
    return json.dumps({"500": "Internal Server Error"}), 500
