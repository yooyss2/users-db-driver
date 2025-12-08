import uuid


def mapping_in(operation, query):

  match operation:

    case "select_customers":

      if query[2] != None:
        if "id" in query[2]:
          query[2]["id"] = uuid.UUID(query[2]["id"]).bytes

    case "select_contacts" | "select_addresses":

      if query[2] != None:
        if "customer_id" in query[2]:
          query[2]["customer_id"] = uuid.UUID(query[2]["customer_id"]).bytes

    case "update_customer":

      if "id" in query[1]:
        query[1]["id"] = uuid.UUID(query[1]["id"]).bytes

  return query


def mapping_out(operation, response):

  if type(response) == tuple:
    fields, data, count = response

  rows = []

  match operation:

    case "select_customers":

      if len(data) > 0:
        for row in data:
          row = list(row)
          row[fields.index("id")] = str(uuid.UUID(bytes=row[fields.index("id")]))
          row[fields.index("birthday")] = str(row[fields.index("birthday")])
          row[fields.index("joindate")] = str(row[fields.index("joindate")])
          rows.append(row)

    case "select_contacts" | "select_addresses":

      if len(data) > 0:
        for row in data:
          row = list(row)
          row[fields.index("customer_id")] = str(uuid.UUID(bytes=row[fields.index("customer_id")]))
          rows.append(row)

  return {"count": count, "fields": fields, "data": rows}
