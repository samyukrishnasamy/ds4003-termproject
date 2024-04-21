# %%
# import dependencies
import pandas as pd
import plotly.express as px
from dash import dash, Dash, dcc, html, Input, Output, callback, callback_context, dash_table, State
from textwrap import wrap



df = pd.read_csv("data.csv")

stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize Dash app
app = Dash(__name__, external_stylesheets=stylesheets, suppress_callback_exceptions=True)

# %%
### add to the dataset ###

sorted_hectares = sorted(df['hectare'].unique())

# Ensure 'date' is a datetime type
df['date'] = pd.to_datetime(df['date'], format='%m%d%Y')

# Count the number of observations per day
observations_per_day = df['date'].value_counts().sort_index()
observations_df = observations_per_day.reset_index()
observations_df.columns = ['date', 'observations']

# %%
#### APP ####

server = app.server

# Navigation bar and page layout
navigation_bar = html.Div([
    html.Div([
        # Buttons
        html.Div([
            html.Button('Home', id='button-0', n_clicks=0, className='btn btn-primary m-1'),
            html.Button('Squirrel Map', id='button-1', n_clicks=0, className='btn btn-primary m-1'),
            html.Button('Activity Graphs', id='button-2', n_clicks=0, className='btn btn-primary m-1'),
            html.Button('Time Graphs', id='button-3', n_clicks=0, className='btn btn-primary m-1'),
            html.Button('More Information', id='button-4', n_clicks=0, className='btn btn-primary m-1'),
        ], style={'display': 'flex', 'gap': '10px'}),
        # GitHub and Original Data Link
        
        html.Div(style={'flexGrow': 1}),
        
        html.Div([
            html.A(
                children=[html.I(className="fab fa-github")],  # FontAwesome icon with text
                href='https://github.com/samyukrishnasamy/ds4003-termproject',
                target='_blank',
                style={'textDecoration': 'none', 'color': 'black', 'marginRight': '20px'}  # Style to make the anchor text look better
            ),
            html.A(
                children="Original Dataset",
                href='https://www.thesquirrelcensus.com/',
                target='_blank',
                style={'textDecoration': 'none', 'color': 'black'}  # Consistent styling for all anchors
            ),
        ], style={'display': 'flex', 'gap': '10px'}),
    ])#, className='d-flex justify-content-between bg-light p-3 rounded')
], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'padding': '10px',
        'backgroundColor': '#f8f9fa',
        'boxShadow': '0 2px 4px rgba(0,0,0,.1)', 
        'position': 'fixed', 
        'width': '100%',
        'zIndex': 1000, 
        'boxSizing': 'border-box', 
    })

font_awesome = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"
app.layout = html.Div(
    html.Div([
        html.Link(rel='stylesheet', href=font_awesome),
        dcc.Location(id='url', refresh=False),
        navigation_bar,
        html.Div(id='page-content'),
    
    ], id='main-layout', style={
        'backgroundImage': 'url(/assets/background.jpg)',
        'backgroundSize': 'cover',
        'backgroundRepeat': 'no-repeat',
        'backgroundPosition': 'center',
        'height': '100vh',
        'width': '100%',
        'overflowY': 'auto',
    })
)

# Callback for updating the page content
@app.callback(
    [Output('page-content', 'children'),
     Output('main-layout', 'style')],
    [Input('button-0', 'n_clicks'), 
     Input('button-1', 'n_clicks'), 
     Input('button-2', 'n_clicks'), 
     Input('button-3', 'n_clicks'), 
     Input('button-4', 'n_clicks')]
)


def display_content(btn0, btn1, btn2, btn3, btn4):
    ctx = callback_context

    if not ctx.triggered:
        button_id = 'button-0'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0] 

    if button_id == 'button-0':
        background_url = '/assets/background.jpg'
    else:
        background_url = '/assets/clouds.jpeg'
    
    style = {
        'backgroundImage': f'url({background_url})',
        'backgroundSize': 'cover',
        'backgroundRepeat': 'no-repeat',
        'backgroundPosition': 'center',
        'height': '100vh',  
        'overflowY': 'auto'
    }
    
    
    # Home Page #
    if button_id == 'button-0':
        content = html.Div([
            #html.H1('Welcome to the Squirrel Dashboard', style={'textAlign': 'center', 'font-family': 'Impact', 'color': 'darkblue'}),
            #html.P("This dashboard provides insights into squirrel sightings in Central Park. Navigate using the buttons above to explore different views and data.", style={'textAlign': 'center'}),
        ])
    
    # Squirrel Map #
    elif button_id == 'button-1':
        content = html.Div([
                html.H1('Squirrel Map', style={'textAlign': 'center', 'font-family': 'Impact', 'color': 'darkblue'}),
                html.P("Spot squirrels in the park with our Squirrel Map! Zoom, click on pins, and learn about our furry friends' locations and colors. It's easy, fun, and gets you closer to nature!", style = {'textAlign': 'center'}),
                html.Label('Select Hectare:'),
                dcc.Dropdown(
                    id='hectare-dropdown',
                    options=[{'label': 'All', 'value': 'All' }] + [{'label': i, 'value': i} for i in sorted_hectares],
                    value='All'
                ),
                dcc.Graph(id = 'squirrel-map'),
        ], style={'padding': '20px'})
    
    # Activity Graphs #
    elif button_id == 'button-2':
        content =  html.Div([
            html.H1('Activity Graphs', style={'textAlign': 'center', 'font-family': 'Impact', 'color': 'darkblue'}),
                # Dropdowns
            html.P("Check out our interactive chart and table for a quick look at squirrel antics in the park. Just choose a location and age, and see the bar chart show the activity levels, while the table gives you all the details at a click.", style = {'textAlign': 'center'}),
            html.Div([
                html.Div([
                # Location
                    html.Label('Select Location'),
                        dcc.Dropdown(
                            id='location',
                            options=[{'label': location, 'value': location} for location in df['location'].unique()],
                            value=["Above Ground"],
                            multi=True,
                        ),
                ], style={'width': '50%'}),
                html.Div([
                # Age
                    html.Label('Select Age:'),
                    dcc.Dropdown(
                        id='age',
                        options=[{'label': age, 'value': age} for age in df['age'].unique()],
                        value=["Adult"],
                        multi=True,                                
                    ),
                ], style={'width': '50%'}),
            ], style={
                    'display': 'flex',
                    'flex-direction': 'row', 
                    'justify-content': 'space-between', 
                    'margin-bottom': '20px' }
                ),
            html.Div([
                html.Div([
                # Bar Graph
                    dcc.Graph(id='activity-graph'),
                ], className='six columns'),     
                html.Div([
                    # Data Table
                    dash_table.DataTable(
                        id='data-table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('records'),
                        style_table={'height': '550px', 'overflowY': 'auto'},
                    )
                ], className='six columns'),           
            ]),                  
        ], style={'margin': '20px'} )
   
   # Time Graphs #
    elif button_id == 'button-3':
        content = html.Div([
            html.H1('Time Graphs', style={'textAlign': 'center', 'font-family': 'Impact', 'color': 'darkblue'}),
            html.P("Dive into our interactive charts: Three pie charts break down the AM and PM patterns for 'kuk', 'quaa', and 'moan' sounds. The line graph displays the number of squirrel sightings over time—use the date slider to focus on the days that interest you!", style = {'textAlign': 'center'}),
            html.Div([
                html.Div([
                # Pie Charts
                dcc.Tabs(id="tabs", value='tab-kuk', children=[
                    dcc.Tab(label='Kuk Sounds', value='tab-kuk'),
                    dcc.Tab(label='Quaa Sounds', value='tab-quaa'),
                    dcc.Tab(label='Moan Sounds', value='tab-moan'),
                ]),
                html.Div(id='tabs-content')
                ], className='six columns'),  # Half the width of the row

            html.Div([
                # Line Graph
                dcc.Graph(id='line-graph', style={'height': '500px'}),
                html.Div([
                    dcc.RangeSlider(
                        id='date-range-slider',
                        min=0,
                        max=len(observations_df) - 1,
                        value=[0, len(observations_df) - 1],
                        marks={i: {'label': str(date.date()), 'style': {'transform': 'rotate(-45deg)', 'white-space': 'nowrap'}}
                            for i, date in enumerate(observations_df['date'])},
                        step=1,
                        pushable=1
                    )
                ], style={'width': '100%', 'padding': '0px 20px', 'marginTop': '20px'}),
            ], className='six columns'),  # Half the width of the row

    ], className='row'),  # This div with className 'row' will hold both columns
], style={'padding': '10px'})
    
   # More Information #
    elif button_id == 'button-4':
        content = html.Div([
            html.H1('More Information', style={'textAlign': 'center', 'font-family': 'Impact', 'color': 'darkblue'}),
            html.Div([
                # Text Column
                html.Div([
                    html.Div([
                        html.H5('Description of Data:', style={'font-family': 'Impact', 'color': 'darkblue'}),
                        html.P('The NYC Squirrel Census data is a unique dataset that provides insights into squirrel populations in Central Park, New York City. The dataset contains squirrel data for 3,023 sightings and includes information such as location, latitude and longitudinal coordinates, age, fur color, activities, and interactions between squirrels and humans.'),
                    ]),
                    html.Div([
                        html.H5('Data Provenance', style={'font-family': 'Impact', 'color': 'darkblue'}),
                        html.P('The data was collected as part of the 2018 Central Park Squirrel Census by a team of volunteers and the Squirrel Census organization. This dataset was published on NYC Open Data. Their purpose was to count and document the squirrel population in Central Park, gather data on their activities and behaviors, and engage the public in both science and nature. The data collection involved visual surveys and standardized data recording practices to ensure consistency and reliability.')
                    ]),
                ], style={'flex': '1'}),  # Texts take up the majority of the space
                
                # GIF Column
                html.Div([
                    html.Img(src='/assets/squirrel-eating.gif', style={'width': '100%', 'height': 'auto'})
                ], style={'flex': '1'}),  # GIF takes up equal space
                
            ], style={'display': 'flex', 'padding': '10px'}),  # Main row using flexbox
        ], style={'padding': '10px'})

    
    return content, style

# %%
### BAR GRAPH ###

age_color_map = {
    'Juvenile': 'lightblue',  # Replace with your actual age group name and desired color
    'Adult': 'darkblue'       # Replace with your actual age group name and desired color
}

@app.callback(
    Output('activity-graph', 'figure'),
    [Input('location', 'value'),  # Ensure this matches your actual Input element ID
     Input('age', 'value')]       # Ensure this matches your actual Input element ID
)
def update_figure(selected_location, selected_age):
    # Filter data based on selected location and age
    filtered_data = df[
        df['location'].isin(selected_location) &
        df['age'].isin(selected_age)
    ]
    # Group by activity and age, and calculate the count for each group
    activity_counts = filtered_data.groupby(['location', 'age']).agg({'running': 'sum', 'chasing': 'sum', 'climbing': 'sum', 
                                                          'eating': 'sum', 'foraging': 'sum'}).reset_index()
    
    # Melt the dataframe to format it for a stacked bar chart
    melted_data = activity_counts.melt(id_vars=['location', 'age'], var_name='Activity', value_name='Count')

    location_str = ', '.join(selected_location) if isinstance(selected_location, list) else selected_location
    age_str = ', '.join(selected_age) if isinstance(selected_age, list) else selected_age
    base_title = "Squirrel Activities"
    subtitle = f"for Location(s): {location_str} and Age(s): {age_str}"

    # Wrap text at 80 characters
    wrapped_subtitle = '<br>'.join(wrap(subtitle, 50))
    title = f"{base_title}<br>{wrapped_subtitle}"

    # Create a stacked bar chart
    fig = px.bar(
        melted_data,
        x='Activity',
        y='Count',
        color='age',  # This will create stacks for each age category within each activity
        pattern_shape='location',  # This will create different patterns for each location
        color_discrete_map=age_color_map,
        title=title,
        labels={'Count': 'Number of Occurrences', 'Activity': 'Squirrel Activity'},
        height=550,
        barmode='stack'
    )
    
    fig.update_layout(
        yaxis_title="Number of Squirrel Occurrences",
        xaxis_title="Age Group"
    )
    
    return fig



# %%
### DATA TABLE ###

@app.callback(
    Output('data-table', 'data'),
    [Input('location', 'value'),
     Input('age', 'value')]
)
def update_table(selected_fur_colors, selected_ages):
    filtered_df = df[df['location'].isin(selected_fur_colors) & df['age'].isin(selected_ages)]
    return filtered_df.to_dict('records')


dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={'height': '250px', 'overflowY': 'auto'}
)

# %%
### MAP ###

@app.callback(
    Output('squirrel-map', 'figure'),
    [Input('hectare-dropdown', 'value')]
)

def update_map(selected_hectare):
    # Set default zoom and center
    zoom = 12
    center_lat = df['lat'].mean()
    center_lon = df['long'].mean()

    # Filter the DataFrame based on the selected hectare
    if selected_hectare and selected_hectare != 'All':
        filtered_df = df[df['hectare'] == selected_hectare]
        print(filtered_df.columns)
        # If a specific hectare is selected, zoom in
        zoom = 17
        # Recenter the map
        center_lat = filtered_df['lat'].mean()
        center_lon = filtered_df['long'].mean()
    else:
        # If 'All' is selected, use the entire DataFrame
        filtered_df = df


    # Define the figure, set color based on the hectare or to dark blue
    if selected_hectare == 'All':
        # Color by hectare if 'All' is selected
        fig = px.scatter_mapbox(
            filtered_df,
            lat='lat',
            lon='long',
            color='hectare',
            hover_data=['unique_squirrel_id', 'primary_fur_color', 'hectare'],
            zoom=zoom,
            color_continuous_scale=px.colors.sequential.Blues
        )
    else:
        # Set to dark blue if a specific hectare is selected
        fig = px.scatter_mapbox(
            filtered_df,
            lat='lat',
            lon='long',
            color_discrete_sequence=['darkblue'],
            hover_data=['unique_squirrel_id', 'primary_fur_color', 'hectare'],
            zoom=zoom
        )
    
    # Update layout of the figure
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_center_lon=center_lon,
        mapbox_center_lat=center_lat,
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    
    return fig

# %%
### PIE CHART ###

@callback(Output('tabs-content', 'children'),
          Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-kuk':
        counts = df[df['sound_kuk']]['shift'].value_counts().reset_index()
        counts.columns = ['shift', 'Count']
        fig = px.pie(counts, 
                     names='shift', 
                     values='Count', 
                     title='Kuk Sounds AM vs PM',
                     color_discrete_sequence=['lightblue', 'darkblue'])
        return html.Div([dcc.Graph(figure=fig)])
    
    elif tab == 'tab-quaa':
        counts = df[df['sound_quaa']]['shift'].value_counts().reset_index()
        counts.columns = ['shift', 'Count']
        fig = px.pie(counts, 
                     names='shift', 
                     values='Count', 
                     title='Quaa Sounds AM vs PM',
                     color_discrete_sequence=['lightblue', 'darkblue'])
        return html.Div([dcc.Graph(figure=fig)])
    
    elif tab == 'tab-moan':
        counts = df[df['sound_moan']]['shift'].value_counts().reset_index()
        counts.columns = ['shift', 'Count']
        fig = px.pie(counts, 
                     names='shift', 
                     values='Count', 
                     title='Moan Sounds AM vs PM',
                     color_discrete_sequence=['lightblue', 'darkblue'])
        return html.Div([dcc.Graph(figure=fig)])


# %%
### LINE GRAPH ###

@app.callback(
    Output('line-graph', 'figure'),
    [Input('date-range-slider', 'value')]
)

def update_line_graph(slider_range):
    filtered_df = observations_df.iloc[slider_range[0]:slider_range[1]+1]

    fig = px.line(
        filtered_df,
        x='date',
        y='observations',
        title='Daily Squirrel Observations',
    )
    return fig

# %%
if __name__ == '__main__':
    app.run_server(debug=True)
    app.run(debug=True, port=8052)

# %% [markdown]
# 

# %%



