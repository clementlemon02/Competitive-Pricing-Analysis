import os
from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get database connection parameters from environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# Create database connection
engine = create_engine(f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

# Sample SQL queries (replace these with your actual queries)
SALES_QUERY = "SELECT * FROM sales"
TOURIST_QUERY = "SELECT * FROM tourists"
RIDERSHIP_QUERY = "SELECT * FROM ridership"
PRICE_QUERY = "SELECT * FROM prices"


def execute_sql_query(query):
    """Execute SQL query and return results."""
    with engine.connect() as connection:
        result = connection.execute(query)
        return [dict(row) for row in result]


@app.route('/sales', methods=['GET'])
def get_sales_data():
    """API endpoint to retrieve sales data."""
    sales_data = execute_sql_query(SALES_QUERY)
    return jsonify(sales_data)


@app.route('/tourist', methods=['GET'])
def get_tourist_data():
    """API endpoint to retrieve tourist data."""
    tourist_data = execute_sql_query(TOURIST_QUERY)
    return jsonify(tourist_data)


@app.route('/ridership', methods=['GET'])
def get_ridership_data():
    """API endpoint to retrieve ridership data."""
    ridership_data = execute_sql_query(RIDERSHIP_QUERY)
    return jsonify(ridership_data)


@app.route('/price', methods=['GET'])
def get_price_data():
    """API endpoint to retrieve price data."""
    price_data = execute_sql_query(PRICE_QUERY)
    return jsonify(price_data)
