import mysql.connector

def start_connection():
  mydb = mysql.connector.connect(
    #WHEN TESTING IN A LOCAL MACHINE
    host="localhost",
    #CONNECTION TO HERR PRIETO'S SERVER:
    #host='192.168.62.137,
    user="siac-admin",
    password="1234",
    database="siac_simple"
  )
  return mydb