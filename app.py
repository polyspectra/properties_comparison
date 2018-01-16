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
    'https://gist.githubusercontent.com/sambozek/5150267fd7dff4249ce789ba60ddd905/raw/38a9a83949dfe9acb9f88ead3da334809dbd9d44/materials.csv')
material_data_values = material_data[['Ultimate Tensile Strength (MPa)', 'Tensile Modulus (GPa)', 'Elongation at Break (%)', 'Flexural Modulus (GPa)', 'Heat Deflection Temperature at 0.455 MPa (oC)', 'Heat Deflection Temperature at 1.82 MPa (oC)']].copy()
material_data_index = material_data[['Name', 'AM Process']].copy()
material_data_columns = list(material_data_values.columns)
material_classes = [{'label': i, 'value': i} for i in material_data['AM Process'].unique()]
material_classes.append(
    {'label': 'All Database Materials', 'value': 'All Database Materials'})

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='Material_Class',
                options=material_classes,
                value='All Database Materials',
                placeholder ='Select Material_Class',  
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
      dash.dependencies.Input('Material_Class', 'value')
     ])
def update_graph(xaxis_column_name, yaxis_column_name, Material_Class):
    
    if Material_Class == 'All Database Materials':
        
        data = {'data': [go.Scatter(
                x=material_data[material_data['AM Process']
                                == i][xaxis_column_name],
                y=material_data[material_data['AM Process']
                                == i][yaxis_column_name],
                text=material_data[material_data['AM Process'] == i]['Supplier'] + '\n' + material_data[material_data['AM Process']
                                                                                                        == i]['Name'] + '\n' + material_data[material_data['AM Process'] == i]['Specific Type'],
                mode='markers',
                name=i,
                visible=True,
                marker={
                    'size': 16,
                    'opacity': 0.6,
                    'line': {'width': 0.1, 'color': 'white'
                             }
                }
                ) for i in material_data['AM Process'].unique()], }
    else:
        data = {'data' : [go.Scatter(
                x=material_data[material_data['AM Process'] == i][xaxis_column_name],
                y=material_data[material_data['AM Process'] == i][yaxis_column_name],
                text=material_data[material_data['AM Process'] == i]['Supplier'] + '\n' + material_data[material_data['AM Process'] == i]['Name'] + '\n' + material_data[material_data['AM Process'] == i]['Specific Type'],
                mode='markers',
                name=i,
                visible=True if i == Material_Class else False,
                marker={
                    'size': 16,
                    'opacity': 0.6,
                    'line': {'width': 0.1, 'color': 'white'
                             }
                }
                ) for i in material_data['AM Process'].unique()],}

    data.update({ 
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
    })

    return data


if __name__ == '__main__':
    app.run_server(debug=True)
