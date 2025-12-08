from .connection import Client, Error
from .datamaps import mapping_in, mapping_out
from .errors import ExecutionError
from .DML import *


cursor = Client.cursor()


def execute(operation, query):
  
  n = 0
  while n <= 1:
    try:
      
      match operation:

        case "select_customers" | "select_contacts" | "select_addresses":

          table = (
            "customers" if operation == "select_customers" else 
            "contacts" if operation == "select_contacts" else
            "addresses" if operation == "select_addresses" else None
          )

          Client.start_transaction()
          
          cursor.execute(*SELECT(table, *mapping_in(operation, query)))

          response = mapping_out(
            operation,
            (
              [field[0] for field in cursor.description],
              cursor.fetchall(),
              cursor.rowcount
            )
          )

          Client.commit()


        case "update_customer":

          for field in ["id", "joindate"]:
            if field in query[0]:
              raise ExecutionError("resricted update on {}".format(field), -1)

          Client.start_transaction()

          cursor.execute(*UPDATE("users", *mapping_in(operation, query)))

          if cursor.rowcount <= 1:

            response = {
              "updated": True if cursor.rowcount == 1 else False,
            }
          
          else:
            Client.rollback()
            raise ExecutionError("updating more than one row on users", -1)

          Client.commit()

      return response
    
    except Error as _err:

      match _err.errno:

        case 2002 | 2013:
          try:
            Client.reconnect(attempts=1, delay=0)
            Client.cmd_init_db(Client.database)
            n += 1
          except Error as __err: ...

      Client.rollback()

      raise Exception(_err.msg, _err.errno)
