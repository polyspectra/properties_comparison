import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os

app = dash.Dash(__name__)
app.title = 'polySpectra Materials Comparison'
server = app.server

material_data = pd.read_csv(
    'https://gist.githubusercontent.com/sambozek/5150267fd7dff4249ce789ba60ddd905/raw/b695e8869d94e64830b12003954471d11420c232/materials.csv')
material_data_values = material_data[['Ultimate Tensile Strength (MPa)', 'Tensile Modulus (GPa)', 'Elongation at Break (%)', 'Flexural Modulus (GPa)', 'Heat Deflection Temperature at 0.455 MPa (oC)', 'Heat Deflection Temperature at 1.82 MPa (oC)']]

material_data.loc[26, 'AM Process'] = 'polySpectra COR Alpha'


#  material_data_index = material_data[['Name', 'AM Process']].copy()
material_data_columns = list(material_data_values.columns)
material_classes = [{'label': i, 'value': i} for i in material_data['AM Process'].unique()]
material_classes.remove(
    {'label':  'polySpectra COR Alpha', 'value': 'polySpectra COR Alpha'})

app.layout = html.Div([
    dcc.Markdown(''' 
# Properties Comparison of Additive Materials
#### Built with love by [polySpectra](http://polyspectra.com)
#### Fork on [Github](https://github.com/polyspectra/properties_comparison)
        '''
    ),
    html.Div([

        html.Div([
            dcc.Checklist(
                id='Material_Class',
                options=material_classes,
                values = [material for material in material_data['AM Process'].unique()],
                # placeholder ='Select Material_Class',  
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

# dcc.Markdown('''
# ##Definitions:

# * **Additive** - Also known as '3D-Printing', where the part is built up layer by layer
#     * **Sintering** - The fusion of powdered materials into solid through use of heat
#     * **Extrusion** - Thermoplastic melted and deposited in layer by layer fashion.
#     * **Photopolymer** - Creation of a solid by exposing liquid to light 
# '''),


])
    

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
      dash.dependencies.Input('Material_Class', 'values')
     ])
def update_graph(xaxis_column_name, yaxis_column_name, Material_Class):
    
    data = {'data' : [go.Scatter(
            x=material_data[material_data['AM Process'] == i][xaxis_column_name],
            y=material_data[material_data['AM Process'] == i][yaxis_column_name],
            text=material_data[material_data['AM Process'] == i]['Supplier'] + '\n' + material_data[material_data['AM Process'] == i]['Name'] + '\n' + material_data[material_data['AM Process'] == i]['Specific Type'],
            mode='markers',
            name=i,
            visible=True,  # if i == Material_Class else False,
            marker={
                'size': 16,
                'symbol': 'star' if i == 'polySpectra COR Alpha' else 'marker', 
                'opacity': 1.0 if i == 'polySpectra COR Alpha' else 0.6,
                'line': {'width': 0.1, 'color': 'white'
                            }
            }
            ) for i in Material_Class],}

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
