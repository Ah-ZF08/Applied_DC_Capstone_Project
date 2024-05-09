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
unique_sites = spacex_df['Launch Site'].unique()
unique_sites = [{'label': site, 'value': site} for site in unique_sites]
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + unique_sites

# Create a dash application
app = dash.Dash(__name__)
# Create an app layout
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Dropdown to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=dropdown_options,
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # Display text
    html.P("Payload range (Kg):"),
    
    # TASK 3: Slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: f'{i} Kg' for i in range(0, 10001, 1000)},
        value=[0, 10000]
    ),
    html.Br(),

    # TASK 4: Scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# Callback for updating the pie chart based on selected launch site
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        filtered_df = spacex_df
        title = "Total Success Launches for All Sites"
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f"Launch Success for Site {selected_site}"

    success_counts = filtered_df['class'].value_counts().reset_index()
    success_counts.columns = ['class', 'count']
    fig = px.pie(
        success_counts,
        values='count',
        names='class',
        title=title,
        color='class',
        color_discrete_map={0: 'red', 1: 'green'}
    )
    return fig

# Callback for updating the scatter chart based on selected launch site and payload range
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter(selected_site, payload_range):
    mask = (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    filtered_df = spacex_df[mask]

    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='BoosterVersion',
        labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Launch Outcome'},
        title=f"Launch Outcomes by Payload Mass at {selected_site if selected_site != 'ALL' else 'All Sites'}",
        hover_data=['BoosterVersion']
    )
    
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
