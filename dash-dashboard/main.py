from database import connect_to_mysql

# Connect to MySQL
success, conn = connect_to_mysql()

if success:
    # Connection was successful
    # Use the connection for database operations
    print("Connection Successful")
else:
    # Connection failed
    # Handle connection error
    print("Connection Failed")

# Close the connection when done
if conn:
    conn.close()
