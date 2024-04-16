import dash
import pandas as pd
from dash import html, dcc, dash_table, callback
import mysql.connector
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar

dash.register_page(__name__, title='MFLG')

# Establish database connection
connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='pwd'
)

common_layout = dict(
    plot_bgcolor='#E6FAD5',  # Change background color here
    font=dict(family='Lora', size=18),
    xaxis=dict(tickfont=dict(family='Lora', size=14)),
    yaxis=dict(tickfont=dict(family='Lora', size=14)),
    legend=dict(font=dict(family='Lora', size=14))
    #paper_bgcolor='#FCFFF9'  # Change paper (plot area) color here
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


# dropdown for month average
year_dropdown = dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': year, 'value': year} for year in rm_df['Year'].unique()],
                    value=[rm_df['Year'].max()],  # Default to the minimum year
                    multi=True  # Allow multiple selections
)

#3. Tourism data 
# Your SQL query to fetch data
tourist_nationality_query = '''
   SELECT Year,'Place of Residence' AS Country,visitor_arrivals
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

# Fetching data from SQL and closing connection
tn_df = pd.read_sql(tourist_nationality_query, connection)
tv_df = pd.read_sql(tourist_volume_query, connection)
ta_df = pd.read_sql(tourist_agegroup_query, connection)

#Convert data format
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


#4. revenue
sales_by_month_query = '''
    SELECT * 
    FROM sales.sales_by_month 
'''
monthly_revenue_df = pd.read_sql(sales_by_month_query, connection)
monthly_revenue_fig = px.line(monthly_revenue_df, x='Month', y='Total', title='Monthly Revenue')
monthly_revenue_fig.update_layout(common_layout)
monthly_revenue_fig.update_traces(line=dict(color='#046845')) 

# for Dropdown and layout
# Define the KPI components and their associated graphs
kpi_components = {
    "Occupancy Rate": {"Histogram of Hourly Ridership":rh_fig,"Ridership Nationalities":nationality_fig},
    "Competitors Prices": {},
    "Revenue": {"Monthly Revenue": monthly_revenue_fig},
    "Tourism":{"Visitors Arrival": tv_fig,"Visitors Nationality":tn_fig,"Age Group Proportion of Visitors":ta_fig}
}

# Create a dropdown menu to select the KPI component
kpi_dropdown = dcc.Dropdown(
    id="kpi-dropdown",
    options=[{"label": kpi, "value": kpi} for kpi in kpi_components.keys()],
    value=list(kpi_components.keys())[0]  # Default to the first KPI component
)

# Define placeholder graphs for the initial display
placeholder_graphs = [
    dcc.Graph(id=f"graph-{i}", figure=go.Figure()) for i in range(len(list(kpi_components.values())[0]))
]

# Dash layout
layout = html.Div([
    html.H1('KPI Dashboard'),
    kpi_dropdown,
    html.Div(id="graphs-container", children=placeholder_graphs),
    html.Br(),

    # Second dropdown within one of the components
    html.Div(year_dropdown, id='rm-dropdown-container', style={'display': 'none'})
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
def update_slider_labels(price_range):
    return f"Current Selection: {price_range[0]} - {price_range[1]}"

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
        rm_fig.add_scatter(x=year_data['Month'], y=year_data['Ridership'], mode='lines', line=dict(dash='dash'), name=f'Year {year}')

    return rm_fig
