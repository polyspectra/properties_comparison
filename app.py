import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import os

app = dash.Dash(__name__)
app.title = 'polySpectra Materials Comparison'
server = app.server

material_data = pd.read_csv(
    'https://gist.githubusercontent.com/sambozek/d3a443cee919da76c10caa5de126b94e/raw/008802685e1a463d9bbe65d4a8980241aee09cee/material_data.csv')
material_data_values = material_data[['Ultimate Tensile Strength (MPa)', 'Tensile Modulus (GPa)', 'Elongation at Break (%)', 'Flexural Modulus (GPa)', 'Heat Deflection Temperature at 0.455 MPa (oC)', 'Heat Deflection Temperature at 1.82 MPa (oC)']].copy()
material_data_index = material_data[['Material Name', 'AM Process']].copy()
material_data_columns = list(material_data_values.columns)

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='Material Class',
                options=[ 
                {'label': i, 'value': i} for i in material_data['AM Process'].unique()
                ],
                value='Additively Manufactured-Photopolymerization',
                placeholder ='Select Material Class',  
            )
            
        ],
        style={'width': '33.33%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in material_data_columns],
                value='Elongation at Break (%)',
                placeholder='Select x-axis parameter'
            )
            
        ],
        style={'width': '33.33%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in material_data_columns],
                placeholder='Select y-axis parameter',
                value='Tensile Modulus (GPa)',

            )
        ],style={'width': '33.33%', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='indicator-graphic'),


])
    

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
      dash.dependencies.Input('Material Class', 'value')
     ])
def update_graph(xaxis_column_name, yaxis_column_name, Material_Class
                ):
    
    return { 
       
            'data': [go.Scatter(
                x=material_data[material_data['AM Process'] == i][xaxis_column_name],
                y=material_data[material_data['AM Process'] == i][yaxis_column_name],
                text=material_data[material_data['AM Process'] == i]['Material Name'],
                mode='markers',
                name=i,
                visible = True if i == Material_Class else False,
                marker={
                    'size': 14 if i == 'Additively Manufatcured-COR-0' else 8,
                    'opacity': 0.6,
                    'line': {'width': 0.1, 'color': 'white'
                     }
                }
                ) for i in material_data['AM Process'].unique()],


        'layout': go.Layout(
            title=Material_Class,
            xaxis={
                    'title': 'Heat Deflection Temperature at 0.455 MPa (<sup>o</sup>C)' if xaxis_column_name == 'Heat Deflection Temperature at 0.455 MPa (oC)' else 'Heat Deflection Temperature at 1.82 MPa (<sup>o</sup>C)' if xaxis_column_name == 'Heat Deflection Temperature at 1.82 MPa (oC)' else xaxis_column_name,
                    'rangemode':'tozero'
            },
            yaxis={
                    'title': 'Heat Deflection Temperature at 0.455 MPa (<sup>o</sup>C)' if yaxis_column_name == 'Heat Deflection Temperature at 0.455 MPa (oC)' else 'Heat Deflection Temperature at 1.82 MPa (<sup>o</sup>C)' if yaxis_column_name == 'Heat Deflection Temperature at 1.82 MPa (oC)' else yaxis_column_name,
                    'rangemode':'tozero'
            },
            margin={'l': 50, 'b': 40, 't': 50, 'r': 50},
            hovermode='closest'

        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
