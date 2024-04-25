import dash
import pandas as pd
from dash import html, dcc, dash_table, callback
import mysql.connector
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar
import requests


common_layout = dict(
    plot_bgcolor='#d8efb4',
    paper_bgcolor='#f7ffea',
    font=dict(family='Lora', size=18),
    xaxis=dict(tickfont=dict(family='Lora', size=14)),
    yaxis=dict(tickfont=dict(family='Lora', size=14)),
    legend=dict(font=dict(family='Lora', size=14))
)

# 1. Occupancy Rate
# Inport data


def fetch_ridership_month():
    response = requests.get('http://127.0.0.1:5000/ridership_by_month')
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        # Handle error
        return []


def fetch_ridership_hour():
    response = requests.get('http://127.0.0.1:5000/ridership_by_hour')
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        # Handle error
        return []


def fetch_rider_nationalities():
    response = requests.get('http://127.0.0.1:5000/rider_nationalities')
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        # Handle error
        return []


rm_df = fetch_ridership_month()
rh_df = fetch_ridership_hour()
nationality_df = fetch_rider_nationalities()

# data manipulation
rm_df['Date'] = pd.to_datetime(rm_df['Date'], format='%m/%d/%Y')
rm_df['Month'] = rm_df['Date'].dt.month_name()
rm_df['Year'] = rm_df['Date'].dt.year

month_order = [calendar.month_name[i] for i in range(1, 13)]
rm_df = rm_df.sort_values(
    by='Month', key=lambda x: pd.Categorical(x, categories=month_order))
monthly_avg = rm_df.groupby(['Month'], as_index=False, sort=False)[
    'Ridership'].mean()
rh_df['Proportion'] = rh_df['Percentile'] * 100

# Create graphs
rm_fig = px.line(monthly_avg, x='Month', y='Ridership',
                 title='Monthly Average Ridership')
rm_fig_div = dcc.Graph(figure=rm_fig,
                       id='monthly-ridership-fig')  # Assign the id to the Div
nationality_fig = px.bar(nationality_df, x='Nationality', y='Percentile',
                         title='Top 5 Riders Nationalities', color_discrete_sequence=['#046845'])
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
    options=[{'label': year, 'value': year}
             for year in rm_df['Year'].unique()],
    value=[pd.to_datetime(x, format='%Y').year for x in ['2022', '2023']],
    multi=True,
    style={
        'color': '#3A3B2C',              # Default text color
        'backgroundColor': '#d8efb4',    # Dropdown background color
        'borderColor': 'black',
        'borderWidth': 'medium',
        'fontWeight': 'bold'
    }
)


@callback(
    Output('monthly-ridership-fig', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_monthly_ridership(selected_years):
    filtered_data = rm_df[rm_df['Year'].isin(selected_years)]
    monthly_avg = filtered_data.groupby(['Month'], as_index=False, sort=False)[
        'Ridership'].mean()
    rm_fig = px.line(monthly_avg, x='Month', y='Ridership',
                     title='Monthly Average Ridership')
    rm_fig.update_layout(common_layout)
    rm_fig.update_traces(line=dict(color='#0F865D'))

    for year in selected_years:
        year_data = filtered_data[filtered_data['Year'] == year]
        rm_fig.add_scatter(x=year_data['Month'], y=year_data['Ridership'], mode='lines',
                           line=dict(dash='dash'), name=f'Year {year}')

    return rm_fig


# 2. Competitors prices
# Fetch min and max prices from the database

def fetch_min_price():
    response = requests.get('http://127.0.0.1:5000/min_price')
    if response.status_code == 200:
        return response.json()
    else:
        # Handle error
        return []


def fetch_max_price():
    response = requests.get('http://127.0.0.1:5000/max_price')
    if response.status_code == 200:
        return response.json()
    else:
        # Handle error
        return []


def fetch_competitor_prices(price_range):
    response = requests.post(
        'http://127.0.0.1:5000/competitor_prices', json=price_range)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        # Handle error
        return []


min_price = fetch_min_price()
max_price = fetch_max_price()

# Competitor Pricings Slider

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
    # Prepare input data, accounting for decimals
    input_data = {
        'min_price': min_price - 1,
        'max_price': max_price + 1
    }
    cp_df = fetch_competitor_prices(input_data)

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


# 3. Revenue

def fetch_monthly_sales():
    response = requests.get('http://127.0.0.1:5000/monthly_sales')
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        # Handle error
        return []


def fetch_monthly_sales():
    response = requests.get('http://127.0.0.1:5000/monthly_sales')
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        # Handle error
        return []


monthly_revenue_df = fetch_monthly_sales()
revenue_df = fetch_monthly_sales()

# Create df grouped by month to obtain data for different years

monthly_revenue_df['Month'] = pd.to_datetime(
    monthly_revenue_df['Month'], format='%b-%y')
monthly_revenue_df['month'] = monthly_revenue_df['Month'].dt.month_name()
monthly_revenue_df['Year'] = monthly_revenue_df['Month'].dt.year

# Remove months without complete years
to_remove = [2021, 2024]

# Create a boolean mask using isin()
mask = monthly_revenue_df['Year'].isin(to_remove)

# Filter the DataFrame using the mask to obtain the points with all 12 mths
year_grp_revenue = monthly_revenue_df[~mask]

monthly_revenue_fig = px.line(monthly_revenue_df, x='Month',
                              y='Total', title='Monthly Revenue (View by Revenue Source)')
monthly_revenue_div = dcc.Graph(
    figure=monthly_revenue_fig, id='monthly-revenue-fig')
monthly_revenue_fig.update_layout(common_layout)
monthly_revenue_fig.update_traces(line=dict(color='#046845'))

year_revenue_fig = px.line(year_grp_revenue, x='Month',
                           y='Total', title='Monthly Revenue (View by Year)')
year_revenue_div = dcc.Graph(figure=year_revenue_fig, id='yearly-revenue-fig')
year_revenue_fig.update_layout(common_layout)
year_revenue_fig.update_traces(line=dict(color='#046845'))


# Update graph to show different revenue types

@callback(
    Output('monthly-revenue-fig', 'figure'),
    [Input('revenue-type-dropdown', 'value')]
)
def update_monthly_revenue(selected_revenue_type):
    monthly_revenue_fig = px.line(
        revenue_df, x='Month', y=selected_revenue_type, title='Monthly Revenue (View by Category)')
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

    year_revenue_fig = px.line(
        revenue_df, x='month', y='Total', title='Monthly Revenue (View by Year)')
    year_revenue_fig.update_layout(common_layout)
    year_revenue_fig.update_traces(line=dict(color='#046845'))

    return year_revenue_fig


revenue_type_dropdown = dcc.Dropdown(
    id="revenue-type-dropdown",
    options=[{"label": revenue_type, "value": revenue_type}
             for revenue_type in ["B2C", "OTC", "Total"]],
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


# 4. Tourism data

def fetch_tourist_nationalities():
    response = requests.get('http://127.0.0.1:5000/tourist_nationalities')
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        # Handle error
        return []


def fetch_tourist_volume():
    response = requests.get('http://127.0.0.1:5000/tourist_volume')
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        # Handle error
        return []


def fetch_tourist_age_group():
    response = requests.get('http://127.0.0.1:5000/tourist_age_group')
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        # Handle error
        return []


tn_df = fetch_tourist_nationalities()
tv_df = fetch_tourist_volume()
ta_df = fetch_tourist_age_group()


# Convert data format
melted_ta_df = pd.melt(ta_df, id_vars='Year',
                       var_name='Age_Group', value_name='Average_Proportion')

months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
tv_df['month'] = pd.Categorical(
    tv_df['month'], categories=months_order, ordered=True)

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
ta_fig.for_each_trace(lambda t: t.update(
    name="Youth" if t.name == "Avg_Y_Prop" else "Adult"))


# For Dropdown and layout
# Define the KPI components and their associated graphs
kpi_components = {
    "Occupancy Rate": {"Histogram of Hourly Ridership": rh_fig, "Ridership Nationalities": nationality_fig},
    "Competitors Prices": {},
    "Revenue": {},
    "Tourism": {"Visitors Arrival": tv_fig, "Visitors Nationality": tn_fig, "Age Group Proportion of Visitors": ta_fig}
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

# Define placeholder graphs for the initial display
placeholder_graphs = [
    dcc.Graph(id=f"graph-{i}", figure=go.Figure()) for i in range(len(list(kpi_components.values())[0]))
]


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
        actual_graphs = []
        if selected_kpi == "Occupancy Rate":
            actual_graphs.append(year_dropdown),
            actual_graphs.append(rm_fig_div)
        elif selected_kpi == "Competitors Prices":
            actual_graphs.append(slider)
            actual_graphs.append(cp_fig_div)
        elif selected_kpi == "Revenue":
            actual_graphs.append(revenue_type_dropdown)
            actual_graphs.append(monthly_revenue_div)
            actual_graphs.append(year_revenue_dropdown)
            actual_graphs.append(year_revenue_div)
        for i, fig in enumerate(figures.values()):
            actual_graphs.append(dcc.Graph(id=f"graph={i}", figure=fig))
        return actual_graphs
    else:
        return placeholder_graphs


# Dash layout
layout = html.Div([
    html.H1('KPI Dashboard'),
    kpi_dropdown,
    html.Br(),
    html.Div(id="graphs-container", children=placeholder_graphs),
    html.Br(),
    # Second dropdown within one of the components
    html.Div(revenue_type_dropdown, id='revenue-dropdown-container',
             style={'display': 'none'}),
    html.Br(),
    html.Div(year_revenue_dropdown,
             id='year-revenue-dropdown-container', style={'display': 'none'})
])
