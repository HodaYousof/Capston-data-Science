import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load Data
data = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Get unique launch sites for dropdown
launch_sites = [{'label': 'All Sites', 'value': 'ALL'}] + \
               [{'label': site, 'value': site} for site in data['Launch Site'].unique()]

# Initialize Dash App
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(children=[
    html.H1("SpaceX Launch Dashboard",
            style={'textAlign': 'left', 'color': '#000000', 'font-size': '24px'}),

    dcc.Dropdown(id='site-dropdown',
                 options=launch_sites,
                 value='ALL',
                 placeholder="Select a launch site",
                 searchable=True),

    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={i: str(i) for i in range(0, 10001, 2000)},
                    value=[0, 10000]),

    dcc.Graph(id='success-pie-chart'),
    dcc.Graph(id='success-payload-scatter-chart')
])


# Callback for Pie Chart
@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(data, values='class', 
                     names='Launch Site', 
                     title='Total Successful Launches for All Sites')
    else:
        filtered_df = data[data['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f'Success vs Failure for {entered_site}')
    return fig


# Callback for Scatter Plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def update_scatter_plot(selected_site, payload_range):
    min_payload, max_payload = payload_range
    filtered_df = data[(data['Payload Mass (kg)'] >= min_payload) & 
                       (data['Payload Mass (kg)'] <= max_payload)]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title=f'Payload vs. Launch Success for {selected_site}',
                     labels={'class': 'Launch Outcome'},
                     hover_data=['Booster Version'])

    return fig


# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
