#%% # Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("2_spacex_launch_dash.csv")

# Create a dash application
app = dash.Dash(__name__)

# Crear los menu dropdown
unicos_launchsites = spacex_df["Launch Site"].unique().tolist()
opciones = [{"label": "All Sites", "value": "ALL"}]
for i in unicos_launchsites:
    opciones.append({'label': i, 'value': i})

#Crear variables para el slider
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div([
                                    # html.Label("Select Statistics:"),
                                    dcc.Dropdown(
                                        id='site-dropdown',
                                        options = opciones,
                                        value = "ALL",
                                        placeholder='Select a Launch Site here',
                                        searchable = True)
                                        ]),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div([dcc.RangeSlider(id='payload-slider',
                                                          min=0, max=10000, step=1000,
                                                          marks={0: '0', 100: '100'},
                                                          value=[min_payload, max_payload])]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df["class"] == 1]
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        fig = px.pie(filtered_df, values='class', 
        names='class', 
        title=f'Total Success Launches fot site {entered_site}')
        return fig
        # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site,slider_values):
    slider_min = slider_values[0]
    slider_max = slider_values[1]
    filtered_df = spacex_df[(spacex_df["Payload Mass (kg)"]>=slider_min) & (spacex_df["Payload Mass (kg)"]<=slider_max)]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df,
                         x="Payload Mass (kg)",
                         y='class',
                         color = 'Booster Version Category', 
        title='Correlation between Payload and Success for all sites')
        return fig
    else:
        # filtered_df = filtered_df[filtered_df["Launch Site"] == entered_site]
        fig = px.scatter(filtered_df,
                     x = "Payload Mass (kg)",
                     y = "class",
                     color ='Booster Version Category',
                     title=f'Correlation between Payload and Success for {entered_site}')
        return fig
        




# Run the app
if __name__ == '__main__':
    app.run_server()
