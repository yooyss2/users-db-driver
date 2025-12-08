def SELECT(table, limit, offset, clauses = None):

  if clauses != None:
    return (
      f"SELECT * FROM {table} WHERE {"AND ".join([f"{clause} = %s" for clause in clauses])} LIMIT %s OFFSET %s",
      [clauses[clause] for clause in clauses] + [limit, offset]
    )
  else:
    return "SELECT * FROM {} LIMIT %s OFFSET %s".format(table), [limit, offset]


# def INSERT(table, data):
#   return (
#     f"INSERT INTO {table} VALUES ({", ".join(["%s" for _ in data])})",
#     [data[value] for value in data]
#   )


def UPDATE(table, values, clauses):
  return (
    f"UPDATE {table} SET {", ".join([f"{value} = %s" for value in values])} " +
    f"WHERE {", ".join([f"{clause} = %s" for clause in clauses])}",
    [values[value] for value in values] + [clauses[clause] for clause in clauses]
  )


def DELETE(table, clauses):
  return (
    f"DELETE FROM {table} WHERE {"AND ".join([f"{clause} = %s" for clause in clauses])}",
    [clauses[clause] for clause in clauses]
  )
