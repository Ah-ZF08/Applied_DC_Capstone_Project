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

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                unique_sites = spacex_df['Launch Site'].unique()
                                unique_sites = [{'label': site, 'value': site} for site in unique_sites]
                                dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + unique_sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=dropdown_options,
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                @app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Filter data for all sites
        filtered_df = spacex_df
        title = "Total Success Launches for All Sites"
    else:
        # Filter data for specific site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f"Launch Success for Site {selected_site}"

    # Prepare data for pie chart
    success_counts = filtered_df['class'].value_counts().reset_index()
    success_counts.columns = ['class', 'count']

    # Create a pie chart
    fig = px.pie(
        success_counts,
        values='count',
        names='class',
        title=title,
        color='class',
        color_discrete_map={0: 'red', 1: 'green'}  # Failed launches in red, successful in green
    )

    return fig
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                payload_slider = dcc.RangeSlider(
    id='payload-slider',
    min=0,
    max=10000,
    step=1000,
    marks={i: f'{i} Kg' for i in range(0, 10001, 1000)},  # Create marks from 0 to 10000 every 1000 Kg
    value=[0, 10000]  # Set the default selected range from minimum to maximum
)





                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter(selected_site, payload_range):
    # Filter data based on selected payload range
    mask = (spacex_df['PayloadMass'] >= payload_range[0]) & (spacex_df['PayloadMass'] <= payload_range[1])
    filtered_df = spacex_df[mask]

    # If a specific launch site is selected (not 'ALL')
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    # Create the scatter plot
    fig = px.scatter(
        filtered_df,
        x='PayloadMass',
        y='class',
        color='BoosterVersion',
        labels={'PayloadMass': 'Payload Mass (kg)', 'class': 'Launch Outcome'},
        title=f"Launch Outcomes by Payload Mass at {selected_site if selected_site != 'ALL' else 'All Sites'}",
        hover_data=['BoosterVersion']
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
