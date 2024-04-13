import dash
from dash import html

# Register the page
dash.register_page(__name__, path='/', title='MFLG')

company_text = """
Mount Faber Leisure Group is a Singapore-based company that focuses on developing and managing leisure and lifestyle attractions. The group is known for its diverse portfolio of offerings, including tourist attractions, entertainment venues, and recreational facilities. Some of its well-known assets include the Singapore Cable Car, Sentosa Merlion, and the Faber Peak Singapore.

The group aims to enhance the leisure and entertainment experiences for both locals and tourists visiting Singapore. Its attractions often highlight the natural beauty of the area while also providing various entertainment and recreational activities for visitors of all ages.
"""

student_text = """
Blablabla
"""


# Create the link component
link = html.A("Mount Faber Leisure Group", href= "https://www.mountfaberleisure.com/", target="_blank")


layout = html.Div([
    html.H1('Introduction'),
    html.P(company_text),
    html.P(student_text),
    html.P("Check out the Mount Faber Leisure Group website: "), 
    link
])

