-- Create the database if it doesn't exist and switch to it
CREATE DATABASE IF NOT EXISTS price_optimization;
USE price_optimization;

-- Create schemas if they don't exist
CREATE SCHEMA IF NOT EXISTS competitor;
CREATE SCHEMA IF NOT EXISTS mflg;
CREATE SCHEMA IF NOT EXISTS tourism;

-- Create table for competitor_prices_data in the competitor schema
CREATE TABLE IF NOT EXISTS competitor.competitor_prices_data (
    attraction VARCHAR(255),
    ticket VARCHAR(255),
    price DECIMAL(10, 2),
    PRIMARY KEY (attraction, ticket) 
);

-- Create tables in the mflg schema
CREATE TABLE IF NOT EXISTS mflg.riders_nationalities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rank INT,
    nationality VARCHAR(255),
    percentage_of_riders DECIMAL(5, 2)
);

CREATE TABLE IF NOT EXISTS mflg.ridership_by_hour (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hour INT,
    ridership INT
);

CREATE TABLE IF NOT EXISTS mflg.ridership_by_month (
    id INT AUTO_INCREMENT PRIMARY KEY,
    period VARCHAR(50), 
    ridership INT
);

CREATE TABLE IF NOT EXISTS mflg.sales_by_month (
    id INT AUTO_INCREMENT PRIMARY KEY,
    month VARCHAR(50),
    b2c DECIMAL(10, 2),
    otc DECIMAL(10, 2),
    total DECIMAL(10, 2)
);

-- Create tables in the tourism schema
CREATE TABLE IF NOT EXISTS tourism.tourist_age_group (
    id INT AUTO_INCREMENT PRIMARY KEY,
    month VARCHAR(50),
    total INT,
    males INT,
    females INT,
    youth INT,
    adult INT,
    youth_percentage DECIMAL(5, 2),
    adult_percentage DECIMAL(5, 2)
);

CREATE TABLE IF NOT EXISTS tourism.tourist_arrival (
    id INT AUTO_INCREMENT PRIMARY KEY,
    arrival_month_year VARCHAR(50),
    visitor_arrivals INT,
    yoy_percentage DECIMAL(5, 2)
);

CREATE TABLE IF NOT EXISTS tourism.tourist_nationalities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    place_of_residence VARCHAR(255),
    visitor_arrivals INT,
    yoy_percentage DECIMAL(5, 2)
);
