#General Timings: 10 AM to 9:30 PM (total arounnd 11.25 hrs)
#Ride Duration: 12 minutes
#Last Admission: 9:15 PM
#Each ride 16 guests
# Compute the occupancy rate by dividing the number of occupied seats or cabins by the total available seats or cabins.

from sys import displayhook
import pandas as pd
from pandas import ExcelFile

ridership_month = pd.read_excel('/Users/rachelloo/Downloads/DSA3101/Competitive-Pricing-Analysis/skyhelix-data/ridership_by_month.xlsx')
ridership_hour = pd.read_excel('/Users/rachelloo/Downloads/DSA3101/Competitive-Pricing-Analysis/skyhelix-data/ridership_by_hour.xlsx')

ridership_month['days_in_month'] = ridership_month['Period'].dt.daysinmonth
# max total capacity of skyhelix per hour = 60/20 * 16 = 48 
# (assumption: time taken for each ride including buffer time is 20minutes)
ridership_month['max_capacity_per_month'] = ridership_month['days_in_month'] * 11.25 * 48
ridership_month['occupancy_rate_per_month'] = (ridership_month["Ridership"] / ridership_month["max_capacity_per_month"]) *100
ridership_month['occupancy_rate_per_month'] = round(ridership_month['occupancy_rate_per_month'], 1) #1dp percentage

displayhook(ridership_month)

#occupancy rate per month based on ridership hour 
# max total capacity of skyhelix per hour = 60/20 * 16 = 48 
ridership_hour["num_of_riders_in_that_hour"] = ridership_hour['Ridership'] * 48
ridership_hour["occupancy_rate_of_hour"] = (ridership_hour['num_of_riders_in_that_hour'] / 48) * 100

displayhook(ridership_hour)