from sys import exit
from os import getpid, getenv
from socket import gethostname, gethostbyname
from platform import platform, architecture

from mysql.connector import (
  connect,
  version,
  Error
)

try:
  connection = connect(
    user="youssef",
    unix_socket="/var/run/mysqld/mysqld.sock",
    # user=getenv("USER"),
    host=getenv("HOST"),
    # unix_socket=getenv("SOCKET"),
    database="customers",
    ssl_disabled=False,
    tls_versions=["TLSv1.3"],
    conn_attrs = {
      "_client_license" : version.LICENSE, 
      "_client_name": "mysqdfdfl-connector-python",
      "_client_version": version.VERSION,
      "_os": platform(),
      "_pid": getpid(),
      "_platform": architecture(),
      "_source_host": gethostbyname(gethostname())
    }
  )

except Error as err:
  if err.errno == 2002:
    print("Can't connect through socket")
  elif (err.errno == 1045 or err.errno == 1524
        or err.msg == "sha256_password requires SSL"):
    print("Could not connect with the given user")
  else:
    print("Something went wrong")

  exit(1)

connection.autocommit = False
connection.get_warnings = False
connection.raise_on_warnings = False

connection.set_charset_collation(charset="utf8mb4", collation="utf8mb4_bin")

Client = connection

del connection
