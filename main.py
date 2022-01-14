
import pandas as pd
import plotly.express as px
import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv("C://Users//Ayotunde//PycharmProjects//Brazil states//states.csv")

dff = df[['State']]
app.layout = html.Div([
    html.Div([
        html.H1(children="States in Brazil Visualization",
                style={
                    'textAlign': 'center',
                    'color': 'Green', }
                )

    ]),
    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=dff.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": False} for i in dff.columns
            ],
            editable=False,
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=6,
            style_cell_conditional=[
                {'if': {'column_id': 'State'},
                 'textAlign': 'left'}
            ],
        ),
    ], className='row'),
    html.Div([
        html.H4(children="Dropdown for Barchart",
                style={
                    'textAlign': 'left',
                    'color': 'Black', }
                )

    ]),

    html.Div([
        html.Div([
            dcc.Dropdown(id='linedropdown',
                         options=[
                             {'label': 'Demographic Density', 'value': 'Demographic Density'},
                             {'label': 'GDP', 'value': 'GDP'}
                         ],
                         value='Demographic Density',
                         multi=False,
                         clearable=False
                         ),
        ], className='six columns'),

        html.Div([
            html.H3(
                children="Bar-chart showing GDP/Demographic density and Population of humans in "
                         "different states of Brazil",
                style={
                    'textAlign': 'center',
                    'color': 'Black'}
                )

        ]),
        html.Div([
            html.Div([
                dcc.Graph(id='linechart'),
            ], className='six columns'),
            html.Div([
                html.H3(children="Pie-chart showing GDP/Count of cities in different states of Brazil",
                        style={
                            'textAlign': 'center',
                            'color': 'Black'}
                        )

            ]),
            html.Div([
                html.H4(children="Dropdown for Piechart",
                        style={
                            'textAlign': 'left',
                            'color': 'Orange', }
                        )

            ]),
            html.Div([
                dcc.Dropdown(id='piedropdown',
                             options=[
                                 {'label': 'Cities count', 'value': 'Cities count'},
                                 {'label': 'GDP', 'value': 'GDP'}
                             ],
                             value='GDP',
                             multi=False,
                             clearable=False
                             ),
            ], className='six columns'),

        ], className='row'),
        html.Div([
            dcc.Graph(id='piechart'),
        ], className='six columns'),

    ], className='row'),

])


@app.callback(
    [Output('piechart', 'figure'),
     Output('linechart', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('linedropdown', 'value')]
)
def update_data(chosen_rows, piedropval, linedropval):
    if len(chosen_rows) == 0:
        df_chosen = df[df['State'].isin(['Alagoas', 'Bahia', 'Roraima', 'Tocantins'])]
    else:
        print(chosen_rows)
        df_chosen = df[df.index.isin(chosen_rows)]

    pie_chart = px.pie(
        data_frame=df_chosen,
        names='State',
        values=piedropval,
        hole=.3,
        labels={'State': 'States in Brazil'}
    )

    # extract list of chosen countries
    list_chosen_countries = df_chosen['State'].tolist()
    # filter original df according to chosen countries
    # because original df has all the complete dates
    df_line = df[df['State'].isin(list_chosen_countries)]

    line_chart = px.bar(
        data_frame=df_line,
        x='Population',
        y=linedropval,
        color='State',
        labels={'State': 'States in Brazil', 'Population': 'Population'},
    )
    line_chart.update_layout(uirevision='foo')

    return pie_chart, line_chart


if __name__ == '__main__':
    app.run_server(debug=True)
