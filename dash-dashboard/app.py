import dash
from dash import Dash, html, dcc

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1('Mount Faber Leisure Group'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)


# Notes:
# Pages are stored in the registry values 
# so to create a new page, remember to include `dash.register_page(__name__)`
# so the .py file is recognized by Dash as a page.