import pandas as pd #(version 0.24.2)
import datetime as dt
import dash         #(version 1.0.0)
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

import plotly       #(version 4.4.1)
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_dark"

df = pd.read_csv("../data/SampleSuperstore.csv")
all_dims = ['Sales', 'Profit']
available_indicators = df['Sub_Category'].unique()

#------------------------------------------------------------------------------------

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server


#-------------------------------------------------------------------------------------
features=df.columns

app.layout = html.Div([

        html.Div([
        html.Br(),
            dbc.Row(dbc.Col(html.Pre(children= "Super Store Sales - USA",
            style={"text-align": "center", "font-size":"300%", "color":"black"}))
        )
        ]),
        html.Div([
        html.Br(),
        dbc.Row(dbc.Col(dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
            #if i == "iso_alpha3" or i == "year" or i == "id"
            #else {"name": i, "id": i, "deletable": True, "selectable": True}
            for i in df.columns
        ],
        data=df.to_dict('records'),  # the contents of the table
        editable=False,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable="single",  # allow users to select 'multi' or 'single' columns
        row_selectable="single",     # allow users to select 'multi' or 'single' rows
        row_deletable=False,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=10,                # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        #style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            #{
                #'if': {'column_id': c},
                #'textAlign': 'left'
            #} for c in ['country', 'iso_alpha3']
        #],
        style_data={                # overflow cells' content into multiple lines
            'plotly_dark': 'normal',
            'height': 'auto'
        }
    )))
    ],style={'padding':10}),

#html.Div([
        html.Div([
        html.Br(),
        dbc.Row(dbc.Col(html.H3("VALUE ANALYSIS ($)"),
                        width={'size': 6, 'offset': 1}
                        )),
        html.Br(),
            dbc.Row(
            [
            dbc.Col(
            (
            html.Label(['X-axis categories to compare:'],style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='xaxis_raditem',
                options=[
                          {'label': 'Segment', 'value': 'Segment'},
                          {'label': 'Region', 'value': 'Region'},
                          {'label': 'State', 'value': 'State'},
                          {'label': 'Category', 'value': 'Category'},
                          {'label': 'Sub-Category', 'value': 'Sub_Category'},
                          {'label': 'Ship Mode', 'value': 'Ship Mode'},
                          {'label': 'Discount', 'value': 'Discount'}
                         ],
                value='Segment',
                #labelStyle={'display': 'inline-block'}
                           )
            ),width={'size': 4, "offset": 1, 'order': 1}
            ),
            dbc.Col(
            (
            html.Label(['Y-axis values to compare:'], style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='yaxis_raditem',
                options=[
                         {'label': 'Sales', 'value': 'Sales'},
                         {'label': 'Profit', 'value': 'Profit'},
                         {'label': 'Loss', 'value': 'Loss'}
                        ],
                value='Sales',
                          )
                     ),width={'size': 3, "offset": 2, 'order': 2}
                   )
            ], no_gutters=True)
            ]),

html.Div(
        [
    html.Br(),
dbc.Row(
       [
dbc.Col(
        dcc.Graph(id='the_graph'),width=8, lg={'size': 6,  "offset": 0, 'order': 'first'}
        ),
dbc.Col(
        dcc.Graph(id='the_graph2'),width=8, lg={'size': 6,  "offset": 0, 'order': 'last'}
        )
        ]
        )
        ],style={'padding':10}),

    html.Div([
    html.Br(),
    html.Br(),

    dbc.Row(dbc.Col(html.H3("REGRESSION ANALYSIS   (Sales Vs Profit)"),
                    width={'size': 6, 'offset': 1},
                    )),
                    html.Br(),
     dbc.Row(
     dbc.Col(
            dcc.Dropdown(
            id='dropdown',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='Phones'),width={'size': 5, "offset": 3, 'order': 1}
                         ))
                         ] ,style={'padding':10}),
    html.Div([
    html.Br(),
    dbc.Row(
            dbc.Col(dcc.Graph(id='the_graph3',
            # style={'width': '100%'},
            # className="column")
            ))
            )
            ],style={'padding':10})
            # style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),


    # html.Div([
    #         dcc.Graph(id='the_graph3',
    #         style={'width': '100%'},
    #         className="column")
    #         ])

 ])



#-------------------------------------------------------------------------------------
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value'),
     Input(component_id='yaxis_raditem', component_property='value')]
     )

def update_graph(x_axis, y_axis):

    dff = df
    # print(dff[[x_axis,y_axis]][:1])
       #colors = ['lightslategray',] * 5
       #colors[1] = 'crimson'
    barchart=px.bar(
            data_frame=dff,
            x=x_axis,
            y=y_axis,
            # log_y=True,
            # log_x=True,
            #color_discrete_sequence =['red']*len(dff),
            labels=dict(Sales="Sales($)"),
            color='Segment',
            title=y_axis+': by '+x_axis,
            #height=400,
            hover_data=["Profit","Discount","Sub_Category","Quantity","Loss"]
            )
    barchart.update_layout(xaxis={'categoryorder':'total ascending'},
                          title={'xanchor':'center', 'yanchor': 'top', 'y':0.9,'x':0.5,}),

    return (barchart)

@app.callback(
              Output(component_id='the_graph2', component_property='figure'),
              [Input(component_id='xaxis_raditem', component_property='value'),
              Input(component_id='yaxis_raditem', component_property='value')]
             )

def update_graph(x_axis, y_axis):
    dff = df

    fig = px.box(dff, x=x_axis,
    y=y_axis,
    log_y=True,
    color='Segment'
)

    return (fig)

#@app.callback(
# def update_bar_chart(x,y,dropdown):
#     fig = px.scatter(
#         df, x=x,y=y,color="Discount",
#         trendline="ols",
#         log_y=True,
#         log_x=True)
#     return fig
@app.callback(
    Output('the_graph3', 'figure'),
    Input('dropdown', 'value'))
def update_figure(selected_category):
    filtered_dff = df[df.Sub_Category == selected_category]

    fig = px.scatter(filtered_dff, x="Sales", y="Profit_Loss",
                     color="Discount",trendline="ols", #hover_name="country",
                     log_x=False,log_y=False, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig
# def update_graph(xaxis_column_name, yaxis_column_name,
#                  xaxis_type):
    # dff = df[df['Year'] == year_value]
    # dff=df
    # return {
    #     'data': [go.Scatter(
    #         x=dff[dff['Sub-Category'] == xaxis_column_name]['Value'],
    #         y=dff[dff['Sub-Category'] == yaxis_column_name]['Value'],
    #         # text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
    #         mode='markers',
    #         marker={
    #             'size': 15,
    #             'opacity': 0.5,
    #             'line': {'width': 0.5, 'color': 'white'}
    #         }
    #     )],
        # 'layout': go.Layout(
        #     xaxis={
        #         'title': xaxis_column_name,
        #         'type': 'linear' if xaxis_type == 'Linear' else 'log'
        #     },
        #     yaxis={
        #         'title': yaxis_column_name,
        #         'type': 'linear' if yaxis_type == 'Linear' else 'log'
        #     },
        #     margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        #     hovermode='closest'
        # )


# def update_graph(xaxis_name, yaxis_name):
#         return {
#             'data': [go.Scatter(
#                 x=df[xaxis_name],
#                 y=df[yaxis_name],
#
#
#                 #text=df['name'],
#                 mode='markers',
#                 marker={
#                     'size': 15,
#                     'opacity': 0.5,
#                     'line': {'width': 0.5, 'color': 'white'}
#                 }
#             )],
#             'layout': go.Layout(
#                 xaxis={'title': xaxis_name.title(),'type': 'log'},
#                 yaxis={'title': yaxis_name.title(),'type': 'log'},
#                 margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
#                 hovermode='closest'
#             )
#         }


if __name__ == '__main__':
    app.run_server(debug=True)
