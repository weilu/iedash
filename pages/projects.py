import dash
from dash import html, dash_table, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd


dash.register_page(__name__)

layout = html.Div(children=[
    dbc.Card(
        dbc.CardBody([
            html.Div(id='projects-content'),
        ])
    )
])


@callback(
    Output('projects-content', 'children'),
    Input('stored-data', 'data'),
    prevent_initial_call=True,
)
def render_table(data):
    projects = pd.DataFrame(data['projects'])
    return dash_table.DataTable(
        id='projects-table',
        columns=[
            {'name': 'Project Id', 'id': 'Project_Id'},
            {'name': 'Project Display Name', 'id': 'Project_Display_Name'},
            {'name': 'Lead Global Practice Code', 'id': 'Lead_Global_Practice_Code'},
            {'name': 'Project Status Name', 'id': 'Project_Status_Name'}
        ],
        data=projects.to_dict('records'),
        filter_action="native",
        sort_action="native",
        page_size=200,
        style_table={'overflowX': 'auto'},  # Scrollable table
        style_cell={'textAlign': 'left'},
        style_header={
            'fontWeight': 'bold',
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgba(0,0,0,0.05)',
            },
        ],
    )


