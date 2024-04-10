import mysql.connector


def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host='localhost',       # Hostname of the MySQL server
            port=3306,              # Port number of the MySQL server (default is 3306)
            user='root',   # Your MySQL username
            password='Troll1234.', # Your MySQL password
            database='test' # Your MySQL database name
        )
        print("Connected to MySQL!")
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    


