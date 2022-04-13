"""# Import dash components"""
from select import select
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

"""#  Import graph plotters"""
import plotly.express as px
import plotly.graph_objects as go

"""# Import processors """
import json
import numpy as np
import pandas as pd

"""# Import dataframes"""
brazil_df = pd.read_csv("data/brazil_df.csv")
states_df = pd.read_csv("data/states_df.csv")

"""#  """
states_df_ = states_df[states_df["data"] == "2022-04-09"]

"""#  """
select_columns = {
    "casosAcumulado" : "Casos Acumulado",
    "casosNovos": "Casos Novos",
    "obitosAcumulado": "Óbitos Totais",
    "obitosNovos": "Óbitos por dia"
}

"""#  """
brazil_states = json.load(open("geojson/brazil_geo.json", "r"))

"""# Istanciação do Dash """
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

"""# Brazil Choroplteh Figure with geojson and style """

fig_brazil_cho = px.choropleth_mapbox(states_df, 
                            locations="estado",
                            color="casosAcumulado",
                            center={"lat": -13.76, "lon": -50.38},
                            geojson=brazil_states,
                            color_continuous_scale="Redor",
                            # opacity=0.4,
                            zoom=4,
                            hover_data= {
                                "casosAcumulado": True, 
                                "casosNovos": True, 
                                "obitosNovos": True, 
                                "estado": True
                                }
                            )
fig_brazil_cho.update_layout(
    mapbox_style="carto-darkmatter",
    autosize=True,
    paper_bgcolor="#242424",
    margin=go.Margin(l=0, r=0, t=0, b=0),
    showlegend=False
)


df_data = states_df[states_df["estado"] == "RJ"]

"""#   Line Figure with cases amount  """

fig_line_ca = go.Figure(
    layout={"template": "plotly_dark"}
)

fig_line_ca.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))

fig_line_ca.update_layout(
    plot_bgcolor="#242424",
    autosize=True,
    paper_bgcolor="#242424",
    margin=dict(l=10, r=10, t=10, b=10)
)

"""#  Criação de Layout """

app.layout = dbc.Container([
        dbc.Row([     
            dbc.Col([
                html.Div([
                    html.Img(id="log", src=app.get_asset_url("logo_dark.png"), height=50),
                    html.H5("Evolução COVID-19"),
                    dbc.Button("BRASIL", color="primary", id="location-button", size="lg")
                ], style={}),
                html.P("Informe a data para recuperar as informações: ", style={"margin-top": "40px"}),
                html.Div(id="div-test", children=[
                    dcc.DatePickerSingle(
                        id= "date-picker",
                        min_date_allowed= brazil_df["data"].min(),
                        max_date_allowed= brazil_df["data"].max(),
                        date= brazil_df["data"].max(),
                        display_format= "MMMM D, YYYY",
                        style={"norder": "0px solid black"}
                    )
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Span("Casos recuperados"),
                                html.H3(style={"color": "#adfc92"}, id="casos-recuperados-text"),
                                html.Span("Em acompanhamento"),
                                html.H5(id="em-acompanhamento-text")

                            ])
                        ], 
                        color="light", 
                        outline=True, 
                        style={
                            "margin-top": "10px",
                            "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19) ",
                            "color": "#FFFFFF"
                        }
                        )
                    ], md=4),

                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Span("Casos confirmados Totais"),
                                html.H3(style={"color": "#389fd6"}, id="casos-confirmados-text"),
                                html.Span("Novos casos na data"),
                                html.H5(id="novos-casos-text")

                            ])
                        ], 
                        color="light", 
                        outline=True, 
                        style={
                            "margin-top": "10px",
                            "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19) ",
                            "color": "#FFFFFF"
                        }
                        )
                    ], md=4),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Span("Óbitos confirmados"),
                                html.H3(style={"color": "#DF2935"}, id="obitos-text"),
                                html.Span("Óbitos na data"),
                                html.H5(id="obitos-na-data-text")

                            ])
                        ], 
                        color="light", 
                        outline=True, 
                        style={
                            "margin-top": "10px",
                            "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19) ",
                            "color": "#FFFFFF"
                        }
                        )
                    ], md=4),
                ]),
                
                html.Div([
                    html.P("Selecione o tipo de dado a visualizar: ", style={"margin-top": "25px"}),
                    dcc.Dropdown(
                        id="location-dropdown",
                        options=[{"label" : j, "value": i} for i, j in select_columns.items()],
                        value="casosNovos",
                        style={"margin-top": "10px"}
                    ),
                    dcc.Graph(id="line-graph", figure=fig_line_ca)
                ]),
            ], md=5, style={"padding": "25px", "background-color": "#242424"}),
            
            dbc.Col([
                dcc.Loading(
                    id="loading-1", 
                    type="default",
                    children=[
                        dcc.Graph(
                            id="choropleth-map", 
                            figure=fig_brazil_cho, 
                            style={"height": "100vh", "margin-right": "10px"}
                        )
                    ]
                )
            ], md=7)
        ])
    ],
fluid=True)

"""#  Functions to interactivity """

"""#  Define outputs and inputs in callback """
@app.callback(
    [
        Output("casos-recuperados-text", "children"),
        Output("em-acompanhamento-text", "children"),
        Output("casos-confirmados-text", "children"),
        Output("novos-casos-text", "children"),
        Output("obitos-text", "children"),
        Output("obitos-na-data-text", "children"),
    ],
    [
        Input("date-picker", "date"), 
        Input("location-button", "children")
    ]
)
def display_status(date, location):
    if location=="BRASIL":
        date_on_date_df = brazil_df[ brazil_df["data"] == date ]
    else:
        date_on_date_df = states_df[( states_df["estado"] == location ) & (states_df["data"] == date)]
    
    recuperados_novos = "-" if date_on_date_df["Recuperadosnovos"].isna().values[0] else f'{int(date_on_date_df["Recuperadosnovos"].values[0]):,}'.replace("," , ".")
    
    casos_acumulado = "-" if date_on_date_df["casosAcumulado"].isna().values[0] else f'{int(date_on_date_df["casosAcumulado"].values[0]):,}'.replace("," , ".")
    
    acompanhamento_novos = "-" if date_on_date_df["emAcompanhamentoNovos"].isna().values[0] else f'{int(date_on_date_df["emAcompanhamentoNovos"].values[0]):,}'.replace("," , ".")
    print(date_on_date_df["emAcompanhamentoNovos"].values[0])
    casos_novos = "-" if date_on_date_df["casosNovos"].isna().values[0]  else f'{int(date_on_date_df["casosNovos"].values[0]):,}'.replace("," , ".")
   
    obitos_acumulado = "-" if date_on_date_df["obitosAcumulado"].isna().values[0] else f'{int(date_on_date_df["obitosAcumulado"].values[0]):,}'.replace("," , ".")
    
    obitos_novos = "-" if date_on_date_df["obitosNovos"].isna().values[0] else f'{int(date_on_date_df["obitosNovos"].values[0]):,}'.replace("," , ".")

    return (
        recuperados_novos, 
        acompanhamento_novos, 
        casos_acumulado, 
        casos_novos, 
        obitos_acumulado, 
        obitos_novos
    )

@app.callback(Output("line-graph", "figure"), [
        Input("location-dropdown", "value"),
        Input("location-button", "children")
] )
def plot_line_graph(plot_type, location):
    if location=="BRASIL":
        date_on_location_df = brazil_df.copy()
    else:
        date_on_location_df = states_df[ states_df["estado"] == location]
    
    bar_plots =["casosNovos", "obitosNovos"]

    fig = go.Figure(layout={"template" : "plotly_dark"})

    if plot_type in bar_plots:
        fig.add_trace(go.Bar(x=date_on_location_df["data"], y=date_on_location_df[plot_type]))
    else:
        fig.add_trace(go.Scatter(x=date_on_location_df["data"], y=date_on_location_df[plot_type]))

    fig.update_layout(
        plot_bgcolor="#242424",
        autosize=True,
        paper_bgcolor="#242424",
        margin=dict(l=10, r=10, t=10, b=10)
    )

    return fig

@app.callback(
    Output("choropleth-map", "figure"),
    [Input("date-picker","date")]
)
def update_map(date):
    date_on_states_df = states_df[states_df["data"] == date]

    fig = px.choropleth_mapbox(date_on_states_df, 
                                locations="estado",
                                color="casosAcumulado",
                                center={"lat": -13.76, "lon": -50.38},
                                geojson=brazil_states,
                                color_continuous_scale="Redor",
                                # opacity=0.84,
                                zoom=4,
                                hover_data= {
                                    "casosAcumulado": True, 
                                    "casosNovos": True, 
                                    "obitosNovos": True, 
                                    "estado": False
                                    }
                            )
    
    fig.update_layout(
        mapbox_style="carto-darkmatter",
        autosize=True,
        paper_bgcolor="#242424",
        margin=go.Margin(l=0, r=0, t=0, b=0),
        showlegend=False
    )

    return fig

@app.callback(
    Output("location-button", "children"),
    [
        Input("choropleth-map", "clickData"), 
        Input("location-button", "n_clicks")
    ]
)
def update_location(click_data, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if click_data is not None and changed_id != "location-button.n_clicks":
        state = click_data["points"][0]["location"]
        return "{}".format(state)
    
    else:
        return "BRASIL"


"""#  Execute  app """
if __name__ == "__main__":
    app.run_server(debug=False)