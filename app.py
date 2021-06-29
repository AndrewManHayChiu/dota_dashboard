import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Can also define in css
colours = {
    'background': 'white',
    'text': 'green'
}

# Define data
df = pd.DataFrame({
    'hero': ['Abaddon', 'Abaddon', 'Abaddon', 'Chaos Knight', 'Lich'],
    'match': [1, 2, 3, 4, 5],
    'kills': [0, 3, 2, 3, 5],
})

# Define charts
# fig = px.bar(data_frame=df, x='Fruit', y='Amount', barmode='group')

fig = px.scatter(data_frame=df, 
                 x='match', y='kills', 
                 color='hero',
                 hover_name='hero')

fig.update_layout(
    plot_bgcolor=colours['background'],
    paper_bgcolor=colours['background'],
    font_color=colours['text']    
)

app.layout = html.Div(style={}, children=[
    html.H1(
        children='Dash(board)',
        style={
            'textAlign': 'left',
        }
    ),
    
    html.Div(
        children='Developing...',
        style={
            'textAlign': 'left'
        }
    ),
    
    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(
        options=[
            {'label': 'Abaddon', 'value': 'Aba'},
            {'label': 'Chaos Knight', 'value': 'CK'},
            {'label': 'Lich', 'value': 'Lich'}
        ],
        value=['Aba', 'CK'],
        multi=True
    ),
    
    dcc.Graph(
        id='scatter_example',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)