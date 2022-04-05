# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

uniques = spacex_df['Launch Site'].unique().tolist()
ls = []
ls.append({'label': 'All Sites', 'value': 'All'})
for s in uniques:
 ls.append({'label': s, 'value': s})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site_dropdown',options=ls,placeholder='Select a Launch Site here', searchable = True , value = 'All Sites'),
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload_slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks = {
                                            0: '0 (kg)',
                                            1000: '1000 (kg)',
                                            2000: '2000 (kg)',
                                            3000: '3000 (kg)',
                                            4000: '4000 (kg)',
                                            5000: '5000 (kg)',
                                            6000: '6000 (kg)',
                                            7000: '7000 (kg)',
                                            8000: '8000 (kg)',
                                            9000: '9000 (kg)',
                                            10000: '10000 (kg)'
                                    },

                                    value=[min_payload,max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
     Output(component_id='success-pie-chart',component_property='figure'),
     [Input(component_id='site_dropdown',component_property='value')]
)
def get_pie_chart(selected_option):
    if (selected_option == 'All'):
        df  = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df, names = 'Launch Site',title = 'Total Success Launches for all sites')
    else:
        df  = spacex_df.loc[spacex_df['Launch Site'] == selected_option]
        fig = px.pie(df, names = 'class',title = 'Total Success Launches for site '+selected_option)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
     Output(component_id='success-payload-scatter-chart',component_property='figure'),
     [Input(component_id='site_dropdown',component_property='value'),Input(component_id="payload_slider", component_property="value")]
)
def get_scattergraph(selected_option,payload_slider):
    if selected_option == 'All':
        low, high = payload_slider
        df  = spacex_df
        f = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[f], x="Payload Mass (kg)", y="class",
            color="Booster Version")
    else:
        low, high = payload_slider
        df  = spacex_df.loc[spacex_df['Launch Site'] == selected_option]
        f = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[f], x="Payload Mass (kg)", y="class",
            color="Booster Version")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
