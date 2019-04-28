import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
import json
from textwrap import dedent as d
from datetime import date, datetime, timedelta
import plotly.graph_objs as go


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div([
        html.H1('Real-time security dashboard'),
        html.Div(id='live-update-text'),
        html.Div(id='live-update-intrusion'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000,
            n_intervals=0
        )
    ]),
    # html.Div([
    #     dcc.Graph(id='hover-graph'),
    #     html.Pre(id='hover-data', style=styles['pre'])
    # ])
])

now = datetime.now()

def load_data():
    with open("payload.json", 'r') as f:
        data = json.load(f)
        return data

@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    style = {'padding': '5px', 'fontSize': '16px'}
    data = load_data()
    events = sum(len(d) for d in data.values())
    return [
        html.Span('Events received: {0:.2f}'.format(events), style=style)
    ]

@app.callback(Output('live-update-intrusion', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_intrusion(n):
    style = {'padding': '5px', 'fontSize': '16px', 'color': 'red'}
    data = load_data()
    guns = len(data['banana']) / 13.0
    return [
        html.Span('Seconds of intrusion detected: {0:.2f}'.format(guns), style=style)
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    data = load_data()
 
    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=1, cols=2, vertical_spacing=0.2)
    # fig['layout']['margin'] = {
    #     'l': 30, 'r': 10, 'b': 30, 't': 10
    # }
    # fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    x = list(data.keys())
    y = [len(d) for d in data.values()]

    fig.append_trace({
        'x': x, 
        'y': y, 
        'type': 'bar'
    }, 1, 1)

    fig.append_trace({
        'x': [x[46]], 
        'y': [y[46]],
        'type': 'bar',
        'marker': dict(color= 'red')
    }, 1, 2)

    return fig

# # Multiple components can update everytime interval gets fired.
# @app.callback(Output('hover-graph', 'figure'),
#               [Input('live-update-graph', 'hoverData')])
# def update_hover_live(hoverData):

#     fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)

#     if hoverData["points"]:
#         points = hoverData["points"]
#         point = points[0]
#         x = point["x"]
#         # print(x)

#         data = load_data()
#         plot_data_x = [to_date(d) for d in data[x]]
#         start = now
#         end = plot_data_x[-1]
#         delta = timedelta(seconds=5)

#         x = []
#         y = []
#         curr = start
#         while curr < end:
#             x.append(curr)
#             count = len([y for y in plot_data_x if y > curr and y < curr + delta])
#             y.append(count)
#             curr += delta

#         fig.append_trace({
#             'x': x, 
#             'y': y, 
#             'type': 'bar'
#         }, 1, 1)
#     return fig

def to_date(data):
    time_data = [int(x) for x in data.split(" ")]
    return datetime(*time_data)


if __name__ == '__main__':
    app.run_server(debug=True)
