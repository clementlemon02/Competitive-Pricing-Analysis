import dash
import pandas as pd
from dash import html, dcc, dash_table,callback
import mysql.connector
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar

dash.register_page(__name__)



# Establish database connection
connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='Lks6712281119@'
)
'''
#1. competitor price
# Fetch data from SQL database
cp_query = """
    SELECT attraction, ticket, price
    FROM (
        SELECT attraction, ticket, price,
                AVG(price) OVER (PARTITION BY attraction) AS mean_price
        FROM competitor.competitor_prices_dataset
    ) AS cp
    ORDER BY mean_price;
"""
cp_df = pd.read_sql(cp_query, connection)

connection.close()



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
cp_fig.add_hline(y=20, line=dict(color='blue', width=2, dash='dash'), annotation_text='Adult', annotation_position='top right')
cp_fig.add_hline(y=17, line=dict(color='red', width=2, dash='dash'), annotation_text='Child', annotation_position='bottom right')

'''
#2. occupancy rate
# inport data
ridership_month_query = '''
    SELECT Period, Ridership,Date
    FROM dsa3101.ridershipbymonth;
    '''

ridership_hour_query = '''
    SELECT Hour, Ridership as Percentile
    FROM dsa3101.ridershipbyhour;
    '''

nationalities_query = '''
    SELECT Nationality, Percentile
    FROM dsa3101.keynationalities;
    '''

tourist_nationality_query = '''
   SELECT Country, Percentage 
   FROM dsa3101.'2023 tourists nationalities`;
'''

rm_df = pd.read_sql(ridership_month_query, connection)
rh_df = pd.read_sql(ridership_hour_query, connection)
nationality_df = pd.read_sql(nationalities_query, connection)


print(rm_df)

# data manipulation
rm_df['Date'] = pd.to_datetime(rm_df['Date'], format='%m/%d/%Y')
rm_df['Month'] = rm_df['Date'].dt.month_name()
rm_df['Year'] = rm_df['Date'].dt.year
month_order = [calendar.month_name[i] for i in range(1, 13)]
rm_df = rm_df.sort_values(by='Month', key=lambda x: pd.Categorical(x, categories=month_order))
monthly_avg = rm_df.groupby(['Month'], as_index=False,sort=False)['Ridership'].mean()

# Create graphs
rm_fig = px.line(monthly_avg, x='Month', y='Ridership', title='Monthly Average Ridership')
rm_fig_div = dcc.Graph(figure=rm_fig,
    id='monthly-ridership-fig')  # Assign the id to the Div
rh_fig=px.line(rh_df, x='Hour', y='Percentile', title='Hourly Average Ridership')
nationality_fig=px.bar(nationality_df, x='Nationality', y='Percentile', title='Nationalities')

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
   SELECT Country, Percentage 
   FROM dsa3101.tourists_nationalities;
'''

tourist_volume_query = '''
    SELECT * 
    FROM dsa3101.tourist_number;
'''

tourist_agegroup_query= '''
SELECT 
    SUBSTR(month, 1, 4) AS Year,
	ROUND(AVG(y_prop), 2) AS Avg_Y_Prop,
    ROUND(AVG(a_prop), 2) AS Avg_A_Prop
FROM
   dsa3101.tourist_age_group
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
connection.close()

#Convert data format
melted_ta_df = pd.melt(ta_df, id_vars='Year', var_name='Age_Group', value_name='Average_Proportion')

# Create plots
tn_fig = px.bar(tn_df, x="Country", y="Percentage", title="Percentage of Individuals Residing in Different Countries")
tv_fig = px.line(tv_df, x="Month", y="Arrivals", title="Number of Visitors in 2023")
ta_fig = px.bar(melted_ta_df, x='Year', y='Average_Proportion', color='Age_Group', barmode='group', 
                 title='Average Proportion of Young and Adult Individuals Between 2021 and 2024')
ta_fig.for_each_trace(lambda t: t.update(name="Young" if t.name == "Avg_Y_Prop" else "Adult"))


# for Dropdown and layout
# Define the KPI components and their associated graphs
kpi_components = {
    "Occupancy Rate": {"Hourly Ridership":rh_fig,"Ridership Nationalities":nationality_fig},
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
        if selected_kpi == "Occupancy Rate":
            # If "Ridership Analysis" KPI is selected, display rm_fig and its dropdown
            actual_graphs = [
                dcc.Graph(id=f"graph-{i}", figure=fig) 
                for i, fig in enumerate(figures.values())
            ]
            # Append the monthly average ridership dropdown to the actual graphs
            actual_graphs.append(year_dropdown),
            actual_graphs.append(rm_fig_div)
        else:
            # For other KPI components, display only the selected figure
            actual_graphs = [
                dcc.Graph(id=f"graph-{i}", figure=fig) 
                for i, fig in enumerate(figures.values())
            ]
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

    for year in selected_years:
        year_data = filtered_data[filtered_data['Year'] == year]
        rm_fig.add_scatter(x=year_data['Month'], y=year_data['Ridership'], mode='lines', line=dict(dash='dash'), name=f'Year {year}')

    return rm_fig
