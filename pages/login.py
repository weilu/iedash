import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State
from flask_login import login_user
from models import User

dash.register_page(__name__)


layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H1('Login', className='text-center mb-4'),
                    dcc.Location(id='url_login'),
                    dbc.Alert(id='login-output', color='danger', is_open=False, className='mt-4'),
                    html.Div([
                        dbc.Label('Email', html_for='username'),
                        dbc.Input(id='username', type='text'),
                    ]),
                    html.Div([
                        dbc.Label('Password', html_for='password'),
                        dbc.Input(id='password', type='password'),
                    ]),
                    dbc.Button('Login', id='login-button', color='primary', className='mt-3'),
                ])
            ]),
            width=6, lg=4, className='mx-auto mt-5'
        )
    ])
])

@callback(
    Output('url_login', 'pathname'),
    Output('login-output', 'children'),
    Input('login-button', 'n_clicks'),
    State('username', 'value'),
    State('password', 'value'),
)
def login_user_click(n_clicks, username, password):
    if n_clicks:
        if not username or not password:
            return None, 'Please enter both username and password'

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return '/projects', ''
        else:
            return None, 'Invalid username or password'
    return None, ''


@callback(
    Output('login-output', 'is_open'),
    Input('login-output', 'children'),
)
def render_error(output_children):
    if output_children:
        return True
    return False
