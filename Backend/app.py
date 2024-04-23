import os
# from urllib import request
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

from pricesimulation.main import run_simulation

load_dotenv() 

app = Flask(__name__)

DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = 3306
DB_NAME = os.getenv("MYSQL_DATABASE")

engine = create_engine(f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
SALES_QUERY = text("SELECT * FROM sales")
VISITOR_QUERY = text("SELECT * FROM annual_visitor")
RIDERSHIP_QUERY = text("SELECT * FROM ridership")
PRICE_QUERY = text("SELECT * FROM prices")
COMPETITOR_PRICES_QUERY = text("SELECT * FROM competitor_prices_dataset")
RIDERSHIP_NATIONALITIES_QUERY = text("SELECT * FROM Key_Nationalities_of_Riders")
RIDERSHIP_BY_HOUR_QUERY = text("SELECT * FROM Ridership_by_Hour")
RIDERSHIP_BY_MONTH_QUERY = text("SELECT * FROM Ridership_by_Month")
MONTHLY_SALES_QUERY = text("SELECT * FROM Sales_by_Month")
TOURIST_AGE_GROUP_QUERY = text("SELECT * FROM tourists_age_group_annual")

def execute_sql_query(query):
    with engine.connect() as connection:
        result = connection.execute(query)
        return result.fetchall()

def test_database_connection():
    try:
        with engine.connect() as connection:
            return True
    except Exception as e:
        print("Failed to connect to the database:", e)
        return False
    
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/visitor', methods=['GET'])
def get_visitor_data():
    visitor_data = execute_sql_query(VISITOR_QUERY)
    formatted_data = []
    for row in visitor_data:
        formatted_data.append({
            'year': row[0],
            'visitor_count': row[1],
        })
    return jsonify(formatted_data)

@app.route('/competitor_prices', methods=['GET'])
def get_competitor_prices():
    competitor_prices = execute_sql_query(COMPETITOR_PRICES_QUERY)
    formatted_data = []
    for row in competitor_prices:
        formatted_data.append({
            'ticket': row[0],
            'price': row[1],
        })
    return jsonify(formatted_data)

@app.route('/ridership_nationalities', methods=['GET'])
def get_ridership_nationalities():
    ridership_nationalities = execute_sql_query(RIDERSHIP_NATIONALITIES_QUERY)
    formatted_data = []
    for row in ridership_nationalities:
        formatted_data.append({
            'Nationality': row[1],
            'Percentage': row[2],
        })
    return jsonify(formatted_data)

@app.route('/ridership_by_hour', methods=['GET'])
def get_ridership_by_hour():
    ridership_by_hour = execute_sql_query(RIDERSHIP_BY_HOUR_QUERY)
    formatted_data = []
    for row in ridership_by_hour:
        formatted_data.append({
            'Hour': row[0],
            'Ridership': row[1],
        })
    return jsonify(formatted_data)

@app.route('/ridership_by_month', methods=['GET'])
def get_ridership_by_month():
    ridership_by_month = execute_sql_query(RIDERSHIP_BY_MONTH_QUERY)
    formatted_data = []
    for row in ridership_by_month:
        formatted_data.append({
            'Period': row[0],
            'Ridership': row[1],
        })
    return jsonify(formatted_data)

@app.route('/monthly_sales', methods=['GET'])
def get_monthly_sales():
    monthly_sales = execute_sql_query(MONTHLY_SALES_QUERY)
    return jsonify(monthly_sales)

@app.route('/tourist_age_group', methods=['GET'])
def get_tourist_age_group():
    tourist_age_group = execute_sql_query(TOURIST_AGE_GROUP_QUERY)
    return jsonify(tourist_age_group)

@app.route('/pricing-simulation', methods=['POST'])
def run_model_endpoint():
    input_data = request.json
    output_data = run_simulation(input_data)  
    return jsonify(output_data)

if __name__ == "__main__":
    if test_database_connection():
        print("Successfully connected to the database!")
    else:
        print("Failed to connect to the database.")
    app.run(host='0.0.0.0')

# if __name__ == "__main__":
#     if test_database_connection():
#         print("Successfully connected to the database!")
#         try:
#             app.run(host='0.0.0.0', debug=False)
#         except KeyboardInterrupt:
#             print("\nServer stopped.")
#     else:
#         print("Failed to connect to the database.")
#     app.run(host='0.0.0.0')
    
