import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from python.Utils import decode


class WebManager:
    def __init__(self):
        self.app = dash.Dash(__name__, assets_folder=os.getcwd() + '/assets', external_stylesheets=["https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/cerulean/bootstrap.min.css"])
        self.server = self.app.server
        self.app.layout = html.Div([
            dbc.Nav([
                html.H1("Image Head Classifier", style={"display": "block"}),
            ], className="navbar navbar-expand-lg navbar-dark bg-dark", style={"height": "100px", "display": "block"}),
            html.Img(src=self.app.get_asset_url('img/figure.png'), style={"margin": "auto", "display": "block"}, alt=""),
            dcc.Upload(
                id='upload-image',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]), style={
                    'width': '100%',
                    'height': '75px',
                    'background': '#b5e4ff',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '20px',
                    'textAlign': 'center',
                    'margin': '25px auto 0 auto'
                }, multiple=True
            ),
            html.Div(id='output-image-upload'),

        ], )

        @self.app.callback(Output('output-image-upload', 'children'),
                           Input('upload-image', 'contents'),
                           State('upload-image', 'filename'))
        def update_output(list_of_contents, list_of_names):
            if list_of_contents is not None:
                children = [WebManager.parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)]
                return children

    def run(self):
        self.app.run_server(debug=True)

    @staticmethod
    def parse_contents(contents, filename):
        from main import get_prediction
        img_array = decode(contents.split(",")[1])
        y_pred = get_prediction(img_array)
        return WebManager.get_html_reply(filename, contents, y_pred)

    @staticmethod
    def get_html_reply(filename, contents, prediction):
        return html.Div(
            [
                html.Div(filename, className="card-header"),
                html.Div(
                    [
                        html.Img(src=contents, style={"width": "300px", "height": "300px", "display": "block"}),
                        dbc.Alert("I think this is a " + prediction, color="primary",
                                  style={"width": "300px", "height": "50px", "display": "block"}),
                    ], className="card-body"),
            ], className="card border-primary mb-3",
            style={"width": "350px", "margin-right": "10px", "display": "inline-block"})
