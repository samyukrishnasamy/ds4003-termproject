# %%
# import dependencies
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback, callback_context

df = pd.read_csv("/Users/samyukrishnasamy/Downloads/data.csv")

# %%
### APP LAYOUT ###
# stylesheet
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# initialize Dash app
app = Dash(__name__, external_stylesheets=stylesheets, suppress_callback_exceptions=True)
server = app.server

navigation_bar = html.Div([
    html.Div([
        # Buttons
        html.Div([
            html.Button('Main Page', id='button-1', className='button'),
            html.Button('Graphs', id='button-2', className='button'),
            html.Button('More Information', id='button-3', className='button'),
        ], style={'display': 'flex'}),
        # Search bar
        html.Div([
            dcc.Input(id='search-input', type='text', placeholder='Search...', className='search-bar'),
            html.Button('Search', id='search-button', className='button')
        ], className='search-container', style={'display': 'flex'}),
    ], className='nav-bar-highlight', style={'display': 'flex', 'justifyContent': 'space-between', 'backgroundColor': '#D3D3D3', 'padding': '10px', 'borderRadius': '5px'}),
], className='nav-bar')

app.layout = html.Div([
    navigation_bar,
    html.Div(id='page-content'),
    html.Div([
        html.H1("A Study of Squirrels in New York", className='twelve columns'),  # title
    ], style={'textAlign': 'center', 'marginTop': '20px'}),
    html.Div([
        html.Div([  # Empty div for the left column
        ], className='six columns'),

        html.Div([
            # Dropdown menus for fur color and age
            html.Div([
                html.Label('Select Fur Color:'),
                dcc.Dropdown(
                    id='fur-color',
                    options=[{'label': color, 'value': color} for color in df['primary_fur_color'].unique()],
                    value=["Gray"],
                    multi=True,
                )
            ], style={'width': '48%', 'display': 'inline-block', 'paddingRight': 10}),
        html.Div([
            html.Label('Select Age:'),
            dcc.Dropdown(
                id='age',
                options=[{'label': age, 'value': age} for age in df['age'].unique()],
                value=["Adult"],
                multi=True,
            )
        ], style={'width': '48%', 'display': 'inline-block', 'paddingRight': 10}),
            
        dcc.Graph(id='activity-graph'),  # Bar graph displaying squirrel activities

        ], className='six columns'),
    ], className='row'),
], style={
    'backgroundImage': 'url(/assets/clouds.jpeg)',
    'backgroundSize': 'cover',
    'backgroundRepeat': 'no-repeat', 
    'height': '150vh',  
    'overflow': 'hidden'
    })


# %%
### GRAPH ###

@app.callback(
    Output('activity-graph', 'figure'),
    [Input('fur-color', 'value'),
     Input('age', 'value')]
)

def update_figure(selected_fur, selected_age):
    filtered_data = df[
        df['primary_fur_color'].isin(selected_fur) &
        df['age'].isin(selected_age)
    ]

    activities = filtered_data[['running', 'chasing', 'climbing', 'eating', 'foraging']].sum().reset_index()
    activity_data = dict(zip(activities['index'], activities[0]))
    activity_df = pd.DataFrame(list(activity_data.items()), columns=['Activity', 'Count'])
    
    fur_str = ', '.join(selected_fur) if isinstance(selected_fur, list) else selected_fur
    age_str = ', '.join(selected_age) if isinstance(selected_age, list) else selected_age

    base_title = "Squirrel Activities"
    subtitle = f"for Fur Color(s): {fur_str} and Age(s): {age_str}"

    title = f"{base_title}\n{subtitle}"


    fig = px.bar(
        activity_df,
        x="Activity", 
        y="Count",
        title=title,
        labels={'Count': 'Number of Occurrences', 'Activity': 'Squirrel Activity'},
        height=550,
        color_discrete_sequence=['Blue']
    )
    
    fig.update_layout(
        yaxis_title="Number of Squirels",
        xaxis_title="Activity Recorded When Encountered"
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug = True)



