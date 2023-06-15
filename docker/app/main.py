#!/usr/bin/env python
# coding: utf-8

# In[172]:


#import required document
import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import Slider, Select


# In[173]:


#read dataset
data = pd.read_csv("./app/melbourne_properties.csv")


# In[174]:


#remove unused columns
data.drop(data.columns[0], axis=1, inplace=True)


# In[175]:


#check NaN Value
data.isnull().sum()


# In[176]:


#fill nan value with median
data.fillna(method ='ffill', inplace = True)


# In[177]:


#check nan value again
data.isnull().sum()


# In[178]:


#remove row that still has nan value
data = data.drop(0)


# In[179]:


#change year column data type to int
data['YearBuilt'] = data['YearBuilt'].apply(int)


# In[180]:


#set yearBuilt as index
data.set_index('YearBuilt', inplace=True)


# In[181]:


#change type values
data = data.replace(['h','t','u'],['house', 'townhouse', 'unit/apartement'])


# In[182]:


# Make a list of the unique values from the type column: property_type_list
property_type_list = data.Type.unique().tolist()

# Make a color mapper: color_mapper
color_mapper = CategoricalColorMapper(factors=property_type_list, palette=Spectral6)


# In[183]:


# Make the ColumnDataSource: source
source = ColumnDataSource(data={
    'x'       : data.loc[1196].Landsize,
    'y'       : data.loc[1196].Price,
    'suburb' : data.loc[1196].Suburb,
    'property types'  : data.loc[1196].Type,
})


# In[184]:


# Create the figure: plot
plot = figure(title='1196', x_axis_label='Land size (m^2)', y_axis_label='Prices (AUD)',
           plot_height=400, plot_width=700, tools=[HoverTool(tooltips='@Type')])

# Add a circle glyph to the figure p
plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
           color=dict(field='property types', transform=color_mapper), legend='property types')

# Set the legend and axis attributes
plot.legend.location = 'bottom_left'


# In[185]:


# Define the callback function: update_plot
def update_plot(attr, old, new):
    # set the `yr` name to `slider.value` and `source.data = new_data`
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    # new data
    new_data = {
    'x'       : data.loc[yr][x],
    'y'       : data.loc[yr][y],
    'suburb' : data.loc[yr].Suburb,
    'property types' : data.loc[yr].Type,
    }
    source.data = new_data
    
    # Add title to figure: plot.title.text
    plot.title.text = 'House built in the year %d' % yr


# In[186]:


# Make a slider object: slider
slider = Slider(start=1196, end=2018, step=1, value=1196, title='Year')
slider.on_change('value',update_plot)


# In[187]:


# Make dropdown menu for x and y axis
# Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=['Rooms', 'Price', 'Bathroom', 'Bedroom2', 'Car', 'Landsize', 'BuildingArea'],
    value='Landsize',
    title='x-axis data'
)
# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['Rooms', 'Price', 'Bathroom', 'Bedroom2', 'Car', 'Landsize', 'BuildingArea'],
    value='Price',
    title='y-axis data'
)
# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update_plot)
    
# Create layout and add to current document
layout = row(widgetbox(slider, x_select, y_select), plot)
curdoc().add_root(layout)

