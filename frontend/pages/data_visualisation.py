import dash 
import pandas as pd 
from dash import html, dcc, dash_table, callback 
import mysql.connector 
from dash.dependencies import Input, Output 
import plotly.express as px 
import plotly.graph_objects as go 
from datetime import datetime 
import calendar 
 
# Establish database connection 
connection = mysql.connector.connect( 
    host='127.0.0.1', 
    port='3306', 
    user='root', 
    password='pwd' 
) 
 
common_layout = dict( 
    plot_bgcolor='#d8efb4',
    paper_bgcolor = '#f7ffea',
    font=dict(family='Lora', size=18), 
    xaxis=dict(tickfont=dict(family='Lora', size=14)), 
    yaxis=dict(tickfont=dict(family='Lora', size=14)), 
    legend=dict(font=dict(family='Lora', size=14))
) 
 
 #1. competitor price 
 # Fetch min and max prices from the database 
min_price_query = "SELECT MIN(price) FROM competitor.competitor_prices_dataset" 
max_price_query = "SELECT MAX(price) FROM competitor.competitor_prices_dataset" 
 
min_price_result = pd.read_sql(min_price_query, connection) 
max_price_result = pd.read_sql(max_price_query, connection) 
 
min_price = min_price_result.iloc[0][0] 
max_price = max_price_result.iloc[0][0] 
 
#2. occupancy rate 
# inport data 
ridership_month_query = ''' 
    SELECT Period, Ridership,Date 
    FROM mflg.ridership_by_month; 
    ''' 
 
ridership_hour_query = ''' 
    SELECT Hour, Ridership as Percentile 
    FROM mflg.ridership_by_hour; 
    ''' 
 
nationalities_query = ''' 
    SELECT Nationality, Percentile 
    FROM mflg.riders_nationalities; 
    ''' 
 
rm_df = pd.read_sql(ridership_month_query, connection) 
rh_df = pd.read_sql(ridership_hour_query, connection) 
nationality_df = pd.read_sql(nationalities_query, connection) 
 
# data manipulation 
rm_df['Date'] = pd.to_datetime(rm_df['Date'], format='%m/%d/%Y') 
rm_df['Month'] = rm_df['Date'].dt.month_name() 
rm_df['Year'] = rm_df['Date'].dt.year 

month_order = [calendar.month_name[i] for i in range(1, 13)] 
rm_df = rm_df.sort_values(by='Month', key=lambda x: pd.Categorical(x, categories=month_order)) 
monthly_avg = rm_df.groupby(['Month'], as_index=False,sort=False)['Ridership'].mean() 
rh_df["Proportion"] = rh_df['Percentile'] * 100 

# Create graphs 
rm_fig = px.line(monthly_avg, x='Month', y='Ridership', title='Monthly Average Ridership') 
rm_fig_div = dcc.Graph(figure=rm_fig, 
    id='monthly-ridership-fig')  # Assign the id to the Div 
nationality_fig=px.bar(nationality_df, x='Nationality', y='Percentile', title='Top 5 Riders Nationalities',color_discrete_sequence=['#046845']) 
rm_fig.update_layout(common_layout) 
rm_fig.update_traces(line=dict(color='#046845'))  
nationality_fig.update_layout(common_layout) 
 
rh_fig = px.histogram(rh_df, x='Hour', y='Proportion', 
                             title='Distribution of Ridership Across Different Hours', 
                             color_discrete_sequence=['#046845']) 
 
# Customize layout 
rh_fig.update_layout(common_layout) 
 
 
# Dropdown for month average 
year_dropdown = dcc.Dropdown( 
                    id='year-dropdown', 
                    options=[{'label': year, 'value': year} for year in rm_df['Year'].unique()], 
                    value= [pd.to_datetime(x, format='%Y').year for x in ['2022','2023']],
                    multi=True,
                    style={
                        'color': '#3A3B2C',               # Default text color
                        'backgroundColor': '#d8efb4',    # Dropdown background color
                        'borderColor': 'black',
                        'borderWidth': 'medium',
                        'fontWeight': 'bold'
                    }
)
 
#3. Tourism data  
tourist_nationality_query = ''' 
   SELECT Year, Country,visitor_arrivals 
   FROM tourism.tourist_nationalities; 
'''
tourist_volume_query = ''' 
    SELECT  
    SUBSTRING(date, 1, 3) AS month, 
    SUBSTRING(date, 5, 8) AS year,  
    visitor_arrivals 
FROM  
   tourism.tourist_arrival; 
''' 
 
tourist_agegroup_query= ''' 
SELECT  
    SUBSTR(month, 1, 4) AS Year, 
  ROUND(AVG(y_prop), 2) AS Avg_Y_Prop, 
    ROUND(AVG(a_prop), 2) AS Avg_A_Prop 
FROM 
   tourism.tourist_age_group 
WHERE  
    SUBSTR(month, 1, 4) BETWEEN '2021' AND '2024' 
GROUP BY  
    SUBSTR(month, 1, 4) 
ORDER BY  
    Year DESC; 
''' 
 
# Fetching data from SQL
tn_df = pd.read_sql(tourist_nationality_query, connection) 
tv_df = pd.read_sql(tourist_volume_query, connection) 
ta_df = pd.read_sql(tourist_agegroup_query, connection) 
 
# Convert data format 
melted_ta_df = pd.melt(ta_df, id_vars='Year', var_name='Age_Group', value_name='Average_Proportion') 
 
months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] 
tv_df['month'] = pd.Categorical(tv_df['month'], categories=months_order, ordered=True) 
 
# Group data by month and calculate the average visitors for each month 
seasonal_data = tv_df.groupby('month')['visitor_arrivals'].mean().reset_index() 
 
# Plot the seasonal data using Plotly Express 
tv_fig = px.line(seasonal_data, x='month', y='visitor_arrivals', title='Seasonal Visitor Arrivals Overview from 2008 to 2024', 
                                labels={'month': 'Month', 'Visitor Arrivals': 'Average Visitors'}) 
tv_fig.update_layout(common_layout) 
tv_fig.update_traces(line=dict(color='#046845'))  
 
tn_fig = px.strip(tn_df, x='Year', y='visitor_arrivals', color='Country', 
                  hover_name='Country', log_x=True,  
                  title='Number of Visitors by Country and Year') 
 
tn_fig.update_layout(common_layout, 
                     yaxis={'categoryorder': 'total ascending'}, 
                     xaxis_title='Year', 
                     yaxis_title='Number of Visitor Arrivals') 
 
ta_fig = px.bar(melted_ta_df, y='Year', x='Average_Proportion', color='Age_Group', barmode='stack',  
                title='Average Proportion of Youth and Adult Individuals Between 2021 and 2024', 
                color_discrete_sequence=['#046845', '#f0aa06']) 
 
ta_fig.update_layout(common_layout) 
ta_fig.for_each_trace(lambda t: t.update(name="Youth" if t.name == "Avg_Y_Prop" else "Adult")) 
 
 
#4. Revenue 
sales_by_month_query = ''' 
    SELECT *  
    FROM mflg.sales_by_month  
''' 
 
sales_by_month_query_b2c = ''' 
    SELECT Month, B2C 
    FROM mflg.sales_by_month  
''' 
 
sales_by_month_query_otc = ''' 
    SELECT Month, OTC 
    FROM mflg.sales_by_month  
''' 
monthly_revenue_df = pd.read_sql(sales_by_month_query, connection) 
monthly_revenue_b2c_df = pd.read_sql(sales_by_month_query_b2c, connection) 
monthly_revenue_otc_df = pd.read_sql(sales_by_month_query_otc, connection) 
 
# Create df grouped by month to obtain data for different years  
monthly_revenue_df['Month'] = pd.to_datetime(monthly_revenue_df['Month'], format='%b-%y') 
monthly_revenue_df['month'] = monthly_revenue_df['Month'].dt.month_name() 
monthly_revenue_df['Year'] = monthly_revenue_df['Month'].dt.year 
# Remove months without complete years 
to_remove = [2021, 2024]  
# Create a boolean mask using isin() 
mask = monthly_revenue_df['Year'].isin(to_remove) 
 
# Filter the DataFrame using the mask to obtain the points with all 12 mths 
year_grp_revenue = monthly_revenue_df[~mask] 
 
monthly_revenue_fig = px.line(monthly_revenue_df, x='Month', y='Total', title='Monthly Revenue (View by Revenue Source)') 
monthly_revenue_div = dcc.Graph(figure=monthly_revenue_fig, id='monthly-revenue-fig')
monthly_revenue_fig.update_layout(common_layout) 
monthly_revenue_fig.update_traces(line=dict(color='#046845'))  
 
year_revenue_fig = px.line(year_grp_revenue, x='Month', y='Total', title='Monthly Revenue (View by Year)') 
year_revenue_div = dcc.Graph(figure=year_revenue_fig, id='yearly-revenue-fig')
year_revenue_fig.update_layout(common_layout) 
year_revenue_fig.update_traces(line=dict(color='#046845'))  
# For Dropdown and layout 
# Define the KPI components and their associated graphs
kpi_components = { 
    "Occupancy Rate": {"Histogram of Hourly Ridership":rh_fig,"Ridership Nationalities":nationality_fig}, 
    "Competitors Prices": {}, 
    "Revenue": {}, 
    "Tourism":{"Visitors Arrival": tv_fig,"Visitors Nationality":tn_fig,"Age Group Proportion of Visitors":ta_fig} 
} 
 
# Create a dropdown menu to select the KPI component 
kpi_dropdown = dcc.Dropdown( 
    id="kpi-dropdown", 
    options=[{"label": kpi, "value": kpi} for kpi in kpi_components.keys()], 
    value=list(kpi_components.keys())[0],  # Default to the first KPI component 
    style={
        'color': '#3A3B2C',
        'backgroundColor': '#d8efb4',
        'borderColor': 'black',
        'borderWidth': 'medium',
        'fontWeight': 'bold'
    }
)
 
 
revenue_type_dropdown = dcc.Dropdown( 
        id="revenue-type-dropdown", 
        options=[{"label": revenue_type, "value": revenue_type} for revenue_type in ["B2C", "OTC", "Total"]], 
        value="OTC",  # Default to total revenue
        style={
        'color': '#3A3B2C',
        'backgroundColor': '#d8efb4',
        'borderColor': 'black',
        'borderWidth': 'medium',
        'fontWeight': 'bold'
        }
    ) 
 
# Dropdown for year  
year_revenue_dropdown = dcc.Dropdown( 
        id="year-revenue-dropdown", 
        options=[{"label": year, "value": year} for year in ["2022", "2023"]], 
        value="2023",  # Default to 2023
        style={
        'color': '#3A3B2C',
        'backgroundColor': '#d8efb4',
        'borderColor': 'black',
        'borderWidth': 'medium',
        'fontWeight': 'bold'
    }
    ) 
 
# Update graph to show different revenue types  
 
@callback( 
    Output('monthly-revenue-fig', 'figure'), 
    [Input('revenue-type-dropdown', 'value')] 
) 
def update_monthly_revenue(selected_revenue_type): 
   # Query the database based on the selected revenue type 
    if selected_revenue_type == "B2C": 
        revenue_query = sales_by_month_query_b2c 
    elif selected_revenue_type == "OTC": 
        revenue_query = sales_by_month_query_otc 
    else: 
        revenue_query = sales_by_month_query 
 
    revenue_df = pd.read_sql(revenue_query, connection) 
    monthly_revenue_fig = px.line(revenue_df, x='Month', y=selected_revenue_type, title='Monthly Revenue (View by Category)') 
    monthly_revenue_fig.update_layout(common_layout) 
    monthly_revenue_fig.update_traces(line=dict(color='#046845')) 
 
    return monthly_revenue_fig 
 
 
# Update graph to show revenue from different years 
 
@callback( 
    Output('yearly-revenue-fig', 'figure'), 
    [Input('year-revenue-dropdown', 'value')] 
) 
def update_year_revenue(selected_year): 
    
    if selected_year == "2022": 
        revenue_df = year_grp_revenue[year_grp_revenue["Year"] == 2022] 
    elif selected_year == "2023": 
        revenue_df = year_grp_revenue[year_grp_revenue["Year"] == 2023] 
     
    year_revenue_fig = px.line(revenue_df, x='month', y='Total', title='Monthly Revenue (View by Year)') 
    year_revenue_fig.update_layout(common_layout) 
    year_revenue_fig.update_traces(line=dict(color='#046845')) 
 
    return year_revenue_fig 
 
# Define placeholder graphs for the initial display 
placeholder_graphs = [ 
    dcc.Graph(id=f"graph-{i}", figure=go.Figure()) for i in range(len(list(kpi_components.values())[0])) 
] 
 
 
# Dash layout 
layout = html.Div([ 
    html.H1('KPI Dashboard'), 
    kpi_dropdown, 
    html.Br(),
    html.Div(id="graphs-container", children=placeholder_graphs), 
    html.Br(), 
    # Second dropdown within one of the components 
    html.Div(revenue_type_dropdown, id='revenue-dropdown-container', style={'display': 'none'}), 
    html.Br(), 
    html.Div(year_revenue_dropdown, id='year-revenue-dropdown-container', style={'display': 'none'}) 
])
 
slider = dcc.RangeSlider( 
        id='price-range', 
        className='slider-bar', 
        min=min_price, 
        max=max_price, 
        step=1, 
        marks=None, 
        value=[min_price, max_price], 
        tooltip={"placement": "bottom", "always_visible": True} 
    ) 
cp_fig_div = dcc.Graph(id='price-boxplot')

# Define callback to update box plot based on price range 
@callback( 
    Output('slider-labels', 'children'), 
    [Input('price-range', 'value')] 
) 
 
# Define callback to update box plot based on price range 
@callback( 
    Output('price-boxplot', 'figure'), 
    [Input('price-range', 'value')] 
) 
def update_boxplot(price_range): 
    min_price, max_price = price_range 
    # Fetch data from SQL database based on price range 
    cp_query = f""" 
         SELECT attraction, ticket, price 
         FROM ( 
             SELECT attraction, ticket, price, 
                     AVG(price) OVER (PARTITION BY attraction) AS mean_price 
             FROM competitor.competitor_prices_dataset 
             WHERE price BETWEEN {min_price-1} AND {max_price+1} 
         ) AS cp 
         ORDER BY mean_price; 
     """ 
    cp_df = pd.read_sql(cp_query, connection) 
 
     # Convert 'attraction' column to categorical data type 
    cp_df['attraction'] = cp_df['attraction'].astype('category') 
 
     # Create box plot 
    cp_fig = px.strip(cp_df, x='attraction', y='price', color='attraction', title='Prices by Attraction', 
                       hover_data=['ticket', 'price'], 
                       labels={ 
                           "attraction": "Attraction", 
                           "price": "Price" 
                       }) 
    # Add horizontal lines for adult and child prices 
    cp_fig.add_hline(y=20, line=dict(color='#046845', width=2, dash='dash'), annotation_text='Adult', 
                      annotation_position='top right') 
    cp_fig.add_hline(y=17, line=dict(color='#F0AA06', width=2, dash='dash'), annotation_text='Child', 
                      annotation_position='bottom right') 
    cp_fig.update_layout(common_layout) 
    
    return cp_fig 
 
 
# Define callback to update selected graph based on dropdown selection 
@callback( 
    Output("graphs-container", "children"), 
    [Input("kpi-dropdown", "value")] 
) 
def update_graphs(selected_kpi): 
    if selected_kpi: 
        # Retrieve the figures associated with the selected KPI component 
        figures = kpi_components[selected_kpi] 
        # Create the actual Plotly graph objects based on the retrieved figures 
        actual_graphs=[] 
        if selected_kpi == "Occupancy Rate": 
            actual_graphs.append(year_dropdown), 
            actual_graphs.append(rm_fig_div) 
        elif selected_kpi =="Competitors Prices": 
            actual_graphs.append(slider) 
            actual_graphs.append(cp_fig_div) 
        elif selected_kpi == "Revenue": 
            actual_graphs.append(revenue_type_dropdown) 
            actual_graphs.append(monthly_revenue_div) 
            actual_graphs.append(year_revenue_dropdown) 
            actual_graphs.append(year_revenue_div) 
        for i, fig in enumerate(figures.values()): 
            actual_graphs.append(dcc.Graph(id=f"graph={i}",figure=fig)) 
        return actual_graphs 
    else: 
        return placeholder_graphs 
 
 
 
@callback( 
    Output('rm-dropdown-container', 'style'), 
    [Input('kpi-dropdown', 'value')] 
) 
def show_component2_dropdown(selected_component): 
    if selected_component == 'Ridership Anaysis': 
        return {'display': 'block'} 
    else: 
        return {'display': 'none'} 
     
 
@callback( 
    Output('monthly-ridership-fig', 'figure'), 
    [Input('year-dropdown', 'value')] 
) 
def update_monthly_ridership(selected_years): 
    filtered_data = rm_df[rm_df['Year'].isin(selected_years)] 
    monthly_avg = filtered_data.groupby(['Month'], as_index=False,sort=False)['Ridership'].mean() 
    rm_fig = px.line(monthly_avg, x='Month', y='Ridership', title='Monthly Average Ridership') 
    rm_fig.update_layout(common_layout) 
    rm_fig.update_traces(line=dict(color='#0F865D'))  
 
    for year in selected_years: 
        year_data = filtered_data[filtered_data['Year'] == year] 
        rm_fig.add_scatter(x=year_data['Month'], y=year_data['Ridership'], mode='lines',
        line=dict(dash='dash'), name=f'Year {year}') 
 
    return rm_fig