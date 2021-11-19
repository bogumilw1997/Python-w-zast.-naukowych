# cd .\lab\lab05\
# poetry run python .\program5.py
# bokeh serve .\program5.py --show

from bokeh.plotting import figure, show, row, column, output_file
from bokeh.io import curdoc
from bokeh.util.hex import hexbin
from bokeh.transform import linear_cmap, factor_cmap
from bokeh.layouts import layout
import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import Spectral10, Plasma10, Cividis10, Turbo256

data = pd.read_json('data/data.json', orient="split")

data.columns = ['Country', 'Deaths_per_million', 'Deaths', 'Cases']

top_df = data.head(10)
countries = top_df['Country'].tolist()

p = figure(x_range=countries, title="COVID-19 Deaths per milion per Country", sizing_mode = 'stretch_width', x_axis_label = 'Country', y_axis_label = 'Deaths per million')
p.vbar(x='Country', top='Deaths_per_million', source=top_df, fill_color=factor_cmap('Country', palette=Spectral10, factors=countries))

hover = HoverTool()
hover.tooltips=[('Country', '@Country'),('Deaths per million', '@Deaths_per_million')]
hover.mode = 'vline'
p.add_tools(hover)


data.sort_values('Deaths', inplace=True, ascending=False)
data = data.iloc[1:]
top_df = data.head(10)
countries = top_df['Country'].tolist()

p2 = figure(x_range=countries, title="COVID-19 Deaths per Country", sizing_mode = 'stretch_width', x_axis_label = 'Country', y_axis_label = 'Deaths')
p2.vbar(x='Country', top='Deaths', source=top_df, fill_color=factor_cmap('Country', palette=Plasma10, factors=countries))

hover = HoverTool()
hover.tooltips=[('Country', '@Country'),('Deaths', '@Deaths')]
hover.mode = 'vline'
p2.add_tools(hover)

data.sort_values('Cases', inplace=True, ascending=False)
data.reset_index()
data.drop(data.index[1])
top_df = data.head(10)
countries = top_df['Country'].tolist()

p3 = figure(x_range=countries, title="COVID-19 Cases per Country", sizing_mode = 'stretch_width', x_axis_label = 'Country', y_axis_label = 'Cases')
p3.vbar(x='Country', top='Cases', source=top_df, fill_color=factor_cmap('Country', palette=Cividis10, factors=countries))

hover = HoverTool()
hover.tooltips=[('Country', '@Country'),('Cases', '@Cases')]
hover.mode = 'vline'
p3.add_tools(hover)

data.sort_values('Deaths_per_million', inplace=True, ascending=False)
countries = data['Country'].tolist()
cmap = linear_cmap('Deaths_per_million', 'Turbo256', 0, data['Deaths_per_million'].max())
p4 = figure(x_range=countries, title="COVID-19 Deaths per milion per Country", sizing_mode = 'stretch_width', x_axis_label = 'Country', y_axis_label = 'Deaths per million')
p4.vbar(x='Country', top='Deaths_per_million', source=data, fill_color=cmap)
hover = HoverTool()
hover.tooltips=[('Country', '@Country'),('Deaths per million', '@Deaths_per_million')]
hover.mode = 'vline'
p4.add_tools(hover)

l = layout(column(p2,p3,p, p4), sizing_mode = 'stretch_width')

curdoc().add_root(l)
