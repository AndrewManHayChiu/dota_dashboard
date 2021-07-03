import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv('data/data.csv')

df

df['match'] = range(len(df))[::-1]
df = df.sort_values('match').drop(columns=['Unnamed: 0'], axis=1)

df

fig = px.line(x=df.match, y=df.deaths, title='Deaths')
fig.show()

px.line(x=df.match, y=df.assists, title='Assists')
px.line(x=df.match, y=df.kills, title='Kills')