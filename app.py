import dash
from dash import html, dcc, Input, Output
from flask import Flask, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_migrate import Migrate
import pages
from models import User, db
from queries import get_projects
import dash_bootstrap_components as dbc


server = Flask(__name__)
server.config['SECRET_KEY'] = 'your_secret_key'
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
server.config['CSRF_ENABLED'] = True

db.init_app(server)
migrate = Migrate(server, db)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Setup Flask-Admin
admin = Admin(server, name='Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.FLATLY, dbc_css],
    suppress_callback_exceptions=True,
    use_pages=True,
)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
}

CONTENT_STYLE = {
    "marginLeft": "14rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem",
}

def get_relative_path(page_name):
    return dash.page_registry[f'pages.{page_name}']['relative_path']


sidebar = html.Div(id='sidebar-content', style=SIDEBAR_STYLE)

content = html.Div(dash.page_container,
    id="page-content", style=CONTENT_STYLE
)

dummy_div = html.Div(id="div-for-redirect")

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    sidebar,
    content,
    dummy_div,
    dcc.Store(id='stored-data'),
])

@app.callback(
    Output('sidebar-content', 'children'),
    [Input('url', 'pathname')]
)
def update_sidebar(pathname):
    links = [
        dbc.NavLink("Home", href=get_relative_path('home'), active="exact"),
    ]
    if current_user.is_authenticated:
        links += [
            dbc.NavLink("Projects", href=get_relative_path('projects'), active="exact"),
            dbc.NavLink("Admin", href='/admin', active="exact"),
            dbc.NavLink("Logout", href='/logout', active="exact"),
        ]
    else:
        links += [
            dbc.NavLink("Login", href='/login', active="exact")
        ]
    return dbc.Nav(links, vertical=True, pills=True)


@app.callback(
    Output('div-for-redirect', 'children'),
    Input('url', 'pathname')
)
def redirect_default(url_pathname):
    if url_pathname == '/logout':
        logout_user()
        return dcc.Location(pathname='/login', id="redirect-me")
    elif url_pathname == '/':
        return dcc.Location(pathname=get_relative_path('home'), id="redirect-me")
    elif url_pathname == get_relative_path('projects') and not current_user.is_authenticated:
        return dcc.Location(pathname='/login', id="redirect-me")
    else:
        return ""


@app.callback(
    Output('stored-data', 'data'),
    Input('stored-data', 'data')
)
def fetch_data_once(data):
    if data is None:
        projects = get_projects()

        return ({
            'projects': projects.to_dict('records'),
        })
    return dash.no_update


if __name__ == '__main__':
    app.run_server(debug=True)

