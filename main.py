import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries

from config import alpha_vantage_key

# -------------------------------------------------------------------------------
# Set up initial key and financial category


# # https://github.com/RomelTorres/alpha_vantage
# # Chose your output format or default to JSON (python dict)
# ts = TimeSeries(alpha_vantage_key, output_format='pandas') # 'pandas' or 'json' or 'csv'
# google_data, google_meta_data = ts.get_intraday(symbol='GOOGL',interval='1min', outputsize='compact')
# df = google_data.copy()
# df = df.transpose()
# df.rename(index={"1. open":"open", "2. high":"high", "3. low":"low",
#                  "4. close":"close","5. volume":"volume"},inplace=True)
# df = df.reset_index().rename(columns={'index': 'indicator'})
# df = pd.melt(df,id_vars=['indicator'], var_name='date', value_name='rate')
# df = df[df['indicator'] != 'volume']
#
# df.to_csv("data.csv", index=False)
# exit()

dff = pd.read_csv('data.csv')
dff = dff[dff.indicator.isin(['high'])]

app = dash.Dash(
        __name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
        meta_tags=[{'name': 'viewport',
                    'content': 'width=device-width, initial_scale=1.0'}]
            )
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardImg(
                    src="/assets/google.svg",
                    top=True,
                    style={"width": "6rem"}
                    ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.P("CHANGE (1D)")
                            ]),
                        dbc.Col([
                            dcc.Graph(
                                id='indicator-graph', figure={},
                                config={'displayModeBar': False}
                                )
                            ])
                        ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='daily-line', figure={},
                                config={'displayModeBar': False}
                                )
                            ])
                        ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("SELL"),
                            ]),
                        dbc.Col([
                            dbc.Button("BUY"),
                            ])
                        ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label(id='low-price', children="12.237"),
                            ]),
                        dbc.Col([
                            dbc.Label(id='high-price', children="13.418")
                            ])
                        ])
                    ])
                ], className="mt-5")
            ], width=11)
        ], justify='center'),

    dcc.Interval(id='update', n_intervals=0, interval=1000*5)

    ])


@app.callback(
        Output('indicator-graph', 'figure'),
        Input('update', 'n_intervals')
        )
def update_graphs(timer):
    dff_rv = dff.iloc[::-1]
    day_start = dff_rv[dff_rv['date'] == dff_rv['date'].min()]['rate'].values[0]
    day_end = dff_rv[dff_rv['date'] == dff_rv['date'].max()]['rate'].values[0]

    fig = go.Figure(go.Indicator(
        mode="delta",
        value=day_end,
        delta={'reference': day_start, 'relative': True, 'valueformat': '.2%'}
        ))
    fig.update_traces(delta_font={'size': 16})
    fig.update_layout(height=40, width=90)

    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='red')
    return fig


# Line Graph
@app.callback(
    Output('daily-line', 'figure'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    dff_rv = dff.iloc[::-1]
    fig = px.line(
            dff_rv,
            x='date',
            y='rate',
            range_y=[dff_rv['rate'].min(), dff_rv['rate'].max()],
            height=120).update_layout(
                    margin=dict(t=0, r=0, l=0, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    yaxis=dict(
                         title=None,
                         showgrid=False,
                         showticklabels=False
                         ),
                    xaxis=dict(
                         title=None,
                         showgrid=False,
                         showticklabels=False
                         ))

    day_start = dff_rv[dff_rv['date'] == dff_rv['date'].min()]['rate'].values[0]
    day_end = dff_rv[dff_rv['date'] == dff_rv['date'].max()]['rate'].values[0]

    if day_end >= day_start:
        return fig.update_traces(fill='tozeroy', line={'color': 'green'})
    elif day_end < day_start:
        return fig.update_traces(fill='tozeroy',
                                 line={'color': 'red'})


# the buttons
@app.callback(
    Output('high-price', 'children'),
    Output('high-price', 'className'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    if timer == 0:
        dff_filtered = dff.iloc[[21, 22]]
        print(dff_filtered)
    elif timer == 1:
        dff_filtered = dff.iloc[[20, 21]]
        print(dff_filtered)
    elif timer == 2:
        dff_filtered = dff.iloc[[19, 20]]
        print(dff_filtered)
    elif timer == 3:
        dff_filtered = dff.iloc[[18, 19]]
        print(dff_filtered)
    elif timer == 4:
        dff_filtered = dff.iloc[[17, 18]]
        print(dff_filtered)
    elif timer == 5:
        dff_filtered = dff.iloc[[16, 17]]
        print(dff_filtered)
    elif timer > 5:
        return dash.no_update

    recent_high = dff_filtered['rate'].iloc[0]
    older_high = dff_filtered['rate'].iloc[1]

    if recent_high > older_high:
        return recent_high, "mt-2 bg-success text-white p-1 border border-primary border-top-0"
    elif recent_high == older_high:
        return recent_high, "mt-2 bg-white p-1 border border-primary border-top-0"
    elif recent_high < older_high:
        return recent_high, "mt-2 bg-danger text-white p-1 border border-primary border-top-0"


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
