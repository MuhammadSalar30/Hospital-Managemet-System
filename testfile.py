import cx_Oracle
TNS_ALIAS = "<alias>"
# Credentials for your Oracle database (replace if needed for educational purposes)
USERNAME = "Sys"
PASSWORD = "Sal321"
try:
  # Connect to the database using the TNS alias and SYSDBA role
  connection = cx_Oracle.connect(f"{USERNAME}/{PASSWORD}@{TNS_ALIAS}", mode=cx_Oracle.SYSDBA)
  # Initialize cursor to None
  cursor = None
  # Execute a simple query to test the connection
  cursor = connection.cursor()
  cursor.execute("SELECT 1 FROM DUAL")  # DUAL is a dummy table in Oracle
  result = cursor.fetchone()
  # Check if the query returned the expected result
  if result[0] == 1:
    print("Successfully connected to Oracle database!")
  else:
    print("Unexpected query result. Connection test failed.")
except cx_Oracle.Error as error:
  print(f"Error connecting to Oracle database: {error}")

finally:
  # Close the cursor and connection if opened
  if cursor:
    cursor.close()
  if connection:
    connection.close()
print("Script execution completed.")
