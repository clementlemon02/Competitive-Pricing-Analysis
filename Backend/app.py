import os
# from urllib import request
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd

from pricesimulation.main import run_simulation

load_dotenv()

app = Flask(__name__)

DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = 3306
DB_NAME = os.getenv("MYSQL_DATABASE")

engine = create_engine(
    f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Occupancy Rate Queries

RIDERSHIP_BY_HOUR_QUERY = text('''  
    SELECT Hour, Ridership  
    FROM ridership_by_hour;  
    ''')

RIDERSHIP_BY_MONTH_QUERY = text('''  
    SELECT Period, Ridership, Date  
    FROM ridership_by_month;  
    ''')

RIDERSHIP_NATIONALITIES_QUERY = text('''  
    SELECT Nationality, Percentile  
    FROM riders_nationalities;  
    ''')

# Competitors Prices Queries

COMPETITOR_PRICES_QUERY = text('''
    SELECT attraction, ticket, price  
        FROM (  
            SELECT attraction, ticket, price,  
                    AVG(price) OVER (PARTITION BY attraction) AS mean_price  
            FROM competitor_prices_dataset  
            WHERE price BETWEEN :min_price AND :max_price
            ) AS cp  
        ORDER BY mean_price;
    ''')
MIN_PRICE_QUERY = text("SELECT MIN(price) FROM competitor_prices_dataset")

MAX_PRICE_QUERY = text("SELECT MAX(price) FROM competitor_prices_dataset")

# Revenue Queries

MONTHLY_SALES_QUERY = text('''  
    SELECT * 
    FROM sales_by_month; 
''')

# Tourism Queries

TOURIST_NATIONALITIES_QUERY = text('''  
   SELECT Year, Country, visitor_arrivals  
   FROM tourist_nationalities;  
''')

TOURIST_VOLUME__QUERY = text('''  
    SELECT   
    SUBSTRING(date, 1, 3) AS month,  
    SUBSTRING(date, 5, 8) AS year,   
    visitor_arrivals  
    FROM   
    tourist_arrival;  
''')

TOURIST_AGE_GROUP_QUERY = text('''  
    SELECT   
    SUBSTR(month, 1, 4) AS Year,  
    ROUND(AVG(y_prop), 2) AS Avg_Y_Prop,  
    ROUND(AVG(a_prop), 2) AS Avg_A_Prop  
    FROM tourist_age_group
    WHERE SUBSTR(month, 1, 4) BETWEEN '2021' AND '2024'  
    GROUP BY   
    SUBSTR(month, 1, 4)  
    ORDER BY   
    Year DESC;  
''')


'''def execute_sql_query(query):
    with engine.connect() as connection:
        result = connection.execute(query)
        return result.fetchall()'''


def execute_sql_query(query, params=None):
    with engine.connect() as connection:
        if params:
            result = connection.execute(query, params)
        else:
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


@app.route('/competitor_prices', methods=['POST'])
def get_competitor_prices():
    request_data = request.json
    # Extract min_price and max_price from the input
    min_price = request_data.get('min_price')
    max_price = request_data.get('max_price')

    competitor_prices = execute_sql_query(
        COMPETITOR_PRICES_QUERY, {'min_price': min_price, 'max_price': max_price})
    formatted_data = []
    for row in competitor_prices:
        formatted_data.append({
            'attraction': row[0],
            'ticket': row[1],
            'price': row[2],
        })
    return jsonify(formatted_data)


@app.route('/min_price', methods=['GET'])
def get_min_price():
    min_price = execute_sql_query(MIN_PRICE_QUERY)
    min_price_value = min_price[0][0]
    return jsonify(min_price_value)


@app.route('/max_price', methods=['GET'])
def get_max_price():
    max_price = execute_sql_query(MAX_PRICE_QUERY)
    max_price_value = max_price[0][0]
    return jsonify(max_price_value)


@app.route('/rider_nationalities', methods=['GET'])
def get_ridership_nationalities():
    ridership_nationalities = execute_sql_query(RIDERSHIP_NATIONALITIES_QUERY)
    formatted_data = []
    for row in ridership_nationalities:
        formatted_data.append({
            'Nationality': row[0],
            'Percentile': row[1],
        })
    return jsonify(formatted_data)


@app.route('/ridership_by_hour', methods=['GET'])
def get_ridership_by_hour():
    ridership_by_hour = execute_sql_query(RIDERSHIP_BY_HOUR_QUERY)
    formatted_data = []
    for row in ridership_by_hour:
        formatted_data.append({
            'Hour': row[0],
            'Percentile': row[1],
        })
    return jsonify(formatted_data)


@app.route('/ridership_by_month', methods=['GET'])
def get_ridership_by_month():
    ridership_by_month = execute_sql_query(RIDERSHIP_BY_MONTH_QUERY)
    formatted_data = []
    for row in ridership_by_month:
        formatted_data.append({
            'Ridership': row[1],
            'Date': row[2],
        })
    return jsonify(formatted_data)


@app.route('/monthly_sales', methods=['GET'])
def get_monthly_sales():
    monthly_sales = execute_sql_query(MONTHLY_SALES_QUERY)
    formatted_data = []
    for row in monthly_sales:
        formatted_data.append({
            'Month': row[0],
            'B2C': row[1],
            'OTC': row[2],
            'Total': row[3],
        })
    return jsonify(formatted_data)


@app.route('/tourist_nationalities', methods=['GET'])
def get_tourist_nationalities():
    tourist_nationalities = execute_sql_query(TOURIST_NATIONALITIES_QUERY)
    formatted_data = []
    for row in tourist_nationalities:
        formatted_data.append({
            'Year': row[0],
            'Country': row[1],
            'visitor_arrivals': row[2],
        })
    return jsonify(formatted_data)


@app.route('/tourist_volume', methods=['GET'])
def get_tourist_volume():
    tourist_volume = execute_sql_query(TOURIST_VOLUME__QUERY)
    formatted_data = []
    for row in tourist_volume:
        formatted_data.append({
            'month': row[0],
            'year': row[1],
            'visitor_arrivals': row[2]
        })
    return jsonify(formatted_data)


@app.route('/tourist_age_group', methods=['GET'])
def get_tourist_age_group():
    tourist_age_group = execute_sql_query(TOURIST_AGE_GROUP_QUERY)
    formatted_data = []
    for row in tourist_age_group:
        formatted_data.append({
            'Year': row[0],
            'Avg_Y_Prop': row[1],
            'Avg_A_Prop': row[2],
        })
    return jsonify(formatted_data)


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
    app.run(host='0.0.0.0', port=5000, debug=True)

    
