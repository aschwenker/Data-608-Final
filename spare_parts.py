# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 21:28:52 2019

@author: ASchwenker
"""
app.layout = html.Div([
    html.H1('Pedestrian Safety near New York City Schools'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Safe Route Schools Map', value='tab-1-example'),
        dcc.Tab(label='Count of Safe Route Schools By Borough', value='tab-2-example'),
        dcc.Tab(label='Accident Density By Borough', value='tab-3-example'),
        dcc.Tab(label='Accident Points', value='tab-4-example')
    ]),
    html.Div(id='tabs-content-example')
])
(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([
            html.H3('Tab content 1'),
            dcc.Graph(id='map', figure=fig)
            ])
    elif tab == 'tab-2-example':
        return html.Div([
            html.H3('Count of Safe Route Schools By Borough'),
            dcc.Graph(
                id='graph',
                figure = {'data': [{
                        'x': ['Bronx', 'Brooklyn','Manhattan','Queens','Staten Island'],
                        'y': [25, 46, 23,33,8],
                        'type': 'bar'
                    }]
                })
        ])

    elif tab == 'tab-3-example':
        return html.Div([
            html.H3('Accident Density By Borough'),
            dcc.Graph(
                id='Accident density',
                figure = accident_density)
        ])
    elif tab == 'tab-4-example':
        return html.Div([
            html.H3('Accident Points'),
            dcc.Graph(id='acc_map', figure=acc_fig),html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='School Districts'
            )],
        style={'width': '48%', 'display': 'inline-block'}),