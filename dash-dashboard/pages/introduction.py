import dash
from dash import html
import dash_bootstrap_components as dbc

# Register the page
dash.register_page(__name__, path='/', title='MFLG')

company_text = """
Mount Faber Leisure Group is a Singapore-based company that focuses on developing and 
managing leisure and lifestyle attractions. The group is known for its diverse portfolio of 
offerings, including tourist attractions, entertainment venues, and recreational facilities. 
Some of its well-known assets include the Singapore Cable Car, SkyHelix Sentosa, and the Faber 
Peak Singapore.

The group aims to enhance the leisure and entertainment experiences for both locals and tourists 
visiting Singapore. Its attractions often highlight the natural beauty of the area while also 
providing various entertainment and recreational activities for visitors of all ages.
"""

student_text_1 = """
We are a group of Data Science and Analytics students from NUS who are working on the price 
optimization of entertainment and attractions. For this project, we will be focusing on price 
optimization for SkyHelix, Singapore's highest open-air panoramic ride. This app consists of 
two main components: a dashboard and a model visualization.
"""

student_text_2 = """
Our dashboard aims to provide insights into our product, from product-specific information 
like occupancy rate and product revenue to factors impacting product performance such as 
competitor prices and tourism information.
"""

student_text_3 = """
On the model visualization page, we will offer business stakeholders the ability to project 
ticket sales and revenue while adjusting for the number of visitors, experimental product price, 
and competitors' prices. The model will also suggest optimal pricing to increase product sales 
and revenue, helping businesses make data-driven decisions on product pricing.
"""

layout = html.Div([
    html.H1('Introduction'),
    html.P(company_text),
    html.P(student_text_1),
    html.P(student_text_2),
    html.P(student_text_3),
    html.P("Check out the Mount Faber Leisure Group website: "),
    dbc.Button("Mount Faber Leisure Group", href="https://www.mountfaberleisure.com/", target="_blank", color="secondary", className="nav-text-selected nav-button-selected mr-1")
], className='intro')  

