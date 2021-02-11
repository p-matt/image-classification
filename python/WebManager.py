import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from python.Utils import memview_base64to_str, base64to_array, get_images_label, get_prediction
from python.Database import get_data_from_db

previous_label = ""
previous_reply = ""
loaded_images = {label: "" for label in get_images_label()}


class WebManager:
    def __init__(self):
        self.app = dash.Dash(__name__, assets_folder=os.getcwd() + '/assets', external_stylesheets=[
            "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/cerulean/bootstrap.min.css"])
        self.server = self.app.server
        self.app.layout = self.get_app_layout()

        # region predictions
        @self.app.callback(Output('output-predict', 'children'),
                           Input('upload-image', 'contents'),
                           State('upload-image', 'filename'))
        def update_output_prediction(list_of_contents, list_of_names):

            if list_of_contents is not None:
                reply = []
                for c, n in zip(list_of_contents, list_of_names):
                    img_array = base64to_array(c)
                    pred = get_prediction(img_array)
                    reply.append(WebManager.get_html_reply_pred(c, n, pred))
                return reply

        # endregion

        # region recherche

        @self.app.callback(
            [Output("output-search", "children"), Output("loading-output-1", "children")],
            [Input('sub', 'n_clicks')], state=[State(component_id='input', component_property='value')]
        )
        def update_output_search(n, input_value):
            global loaded_images
            if input_value is not None and len(input_value) >= 3:
                matching_label = [label for label in get_images_label() if
                                  input_value.lower() in label.lower().replace("head", "")]
                if len(matching_label):
                    label = matching_label[0]
                    if loaded_images[label] != "" and loaded_images[label] != "loading":
                        return loaded_images[label], ""
                    elif loaded_images[label] != "loading":
                        loaded_images[label] = "loading"
                        reply = []
                        rows = get_data_from_db(label)
                        for row in rows:
                            str_64 = "data:image/jpeg;base64,{}".format(memview_base64to_str(row[0]))
                            reply.append(WebManager.get_html_reply_search(str_64))
                        loaded_images[label] = reply
                        return loaded_images[label], ""
                    return loaded_images[label], ""
            return "", ""

        # endregion

    def run(self):
        self.app.run_server(debug=False)

    @staticmethod
    def get_html_reply_pred(content, filename, prediction):
        return html.Div(
            [
                html.Div(filename, className="card-header"),
                html.Div(
                    [
                        html.Img(src=content, style={"width": "100%", "height": "300px", "display": "block"}),
                        dbc.Alert("I think this is a " + prediction, color="primary",
                                  style={"width": "100% ", "height": "50px", "display": "block"}),
                    ], className="card-body"),
            ], className="card border-primary mb-3",
            style={"margin-right": "15px", "display": "inline-block", "width": "48%"})

    @staticmethod
    def get_html_reply_search(img_base64):
        return html.Div(
            [
                html.Div(
                    [
                        html.Img(src=img_base64, style={"width": "100%", "height": "300px", "display": "block"}),
                    ], className="card-body"),
            ], className="card", style={"width": "33.3%", "display": "inline-block"})

    def get_app_layout(self):
        return html.Div([
            dbc.Nav([
                html.H1("Image Head Classifier", style={"display": "block"}),
            ], className="navbar navbar-expand-lg navbar-dark bg-dark", style={"height": "100px", "display": "block"}),
            html.Img(src=self.app.get_asset_url('img/figure.png'),
                     style={"margin": "25px auto", "display": "block"}, alt=""),
            html.Div([
                dcc.Upload(
                    id='upload-image',
                    style={
                        'width': '90%', "display": "block", 'height': '75px', 'background': '#b5e4ff',
                        'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '20px',
                        'textAlign': 'center', 'margin': '0 auto'
                    }, multiple=True,
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                ),
                html.Div(id='output-predict', style={"display": "block", "margin": "auto", "width": "90%"}),
            ], id="predictions", style={"width": "49%", "display": "inline-block", "vertical-align": 'top'}),
            html.Div([
                dcc.Input(id="input", type="text", className="form-control",
                          placeholder="Enter a name from the aboves ones",
                          style={"width": "80%", "type": "submit", "display": "inline-block"}),
                html.Button('Search', className="btn btn-primary", id='sub',
                            style={"width": "20%", "vertical-align": "top", "display": "inline-block"}),
                dcc.Loading(id="loading-1", type="default", style={"margin-top": "3em"}, children=html.Div(id="loading-output-1")),
                html.Div(id='output-search', style={"margin-top": "3em"}),
            ], id="search", style={"display": "inline-block", "margin-top": "1em", "width": "49%"}),
        ], )
