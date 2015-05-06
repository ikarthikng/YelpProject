__author__ = 'Karthik'
"""
Yelp Data Set Challenge
There are several files used for this project. Each files contains JSON data each line.

Files given:
yelp_academic_dataset_business.json

{
    'type': 'business',
    'business_id': (encrypted business id),
    'name': (business name),
    'neighborhoods': [(hood names)],
    'full_address': (localized address),
    'city': (city),
    'state': (state),
    'latitude': latitude,
    'longitude': longitude,
    'stars': (star rating, rounded to half-stars),
    'review_count': review count,
    'categories': [(localized category names)]
    'open': True / False (corresponds to closed, not business hours),
    'hours': {
        (day_of_week): {
            'open': (HH:MM),
            'close': (HH:MM)
        },
        ...
    },
    'attributes': {
        (attribute_name): (attribute_value),
        ...
    },
}

yelp_academic_dataset_checkin.json

{
    'type': 'checkin',
    'business_id': (encrypted business id),
    'checkin_info': {
        '0-0': (number of checkins from 00:00 to 01:00 on all Sundays),
        '1-0': (number of checkins from 01:00 to 02:00 on all Sundays),
        ...
        '14-4': (number of checkins from 14:00 to 15:00 on all Thursdays),
        ...
        '23-6': (number of checkins from 23:00 to 00:00 on all Saturdays)
    }, # if there was no checkin for a hour-day block it will not be in the dict
}

yelp_academic_dataset_review.json

{
    'type': 'review',
    'business_id': (encrypted business id),
    'user_id': (encrypted user id),
    'stars': (star rating, rounded to half-stars),
    'text': (review text),
    'date': (date, formatted like '2012-03-14'),
    'votes': {(vote type): (count)},
}

yelp_academic_dataset_tip.json

{
    'type': 'tip',
    'text': (tip text),
    'business_id': (encrypted business id),
    'user_id': (encrypted user id),
    'date': (date, formatted like '2012-03-14'),
    'likes': (count),
}

yelp_academic_dataset_user.json

{
    'type': 'user',
    'user_id': (encrypted user id),
    'name': (first name),
    'review_count': (review count),
    'average_stars': (floating point average, like 4.31),
    'votes': {(vote type): (count)},
    'friends': [(friend user_ids)],
    'elite': [(years_elite)],
    'yelping_since': (date, formatted like '2012-03'),
    'compliments': {
        (compliment_type): (num_compliments_of_this_type),
        ...
    },
    'fans': (num_fans),
}
"""
import json
import timeit
from bokeh.browserlib import view
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.models.glyphs import Circle
from bokeh.models import (GMapPlot, Range1d, ColumnDataSource, LinearAxis,
                        PanTool, WheelZoomTool, BoxSelectTool, BoxSelectionOverlay,
                        GMapOptions, NumeralTickFormatter, PrintfTickFormatter, HoverTool)
from bokeh.resources import INLINE
import re

#Business file name
business_filename = "yelp_academic_dataset_business.json"

#Counter to keep track of number of business needs to be displayed on the map
counter = 0
#Declare all the local variables
latitude=[]
longitude=[]
business_name = []
stars = []
color = []

#Obtain the visaulizaiton of
with open(business_filename) as filename:
    for user_data in filename:
        json_obj = json.loads(user_data)
        #Remove all punctuations from the name because the rendering in the HTML was not proper
        name = re.sub('[^A-Za-z0-9]+', ' ', json_obj['name'])
        business_name.append(name)
        rating = json_obj['stars']
        stars.append(json_obj['stars'])
        latitude.append(json_obj['latitude'])
        longitude.append(json_obj['longitude'])
        #Based on rating, give an appropriate color to the business
        if 4 <= rating <= 5:
            cr = "green"
        elif 3 <= rating <= 4:
            cr = "yellow"
        elif 2 <= rating <= 3:
            cr = "orange"
        elif 1 <= rating <= 2:
            cr = "red"

        color.append(cr)

        if counter == 100000:
            break
        counter += 1

#Specify the X and Y axis
x_range = Range1d()
y_range = Range1d()

#This will display the USA map
map_options = GMapOptions(lat=37.09024, lng=-95.712891, zoom=4)

#Details of the plot
plot = GMapPlot(x_range=x_range, y_range=y_range,map_options=map_options,
                title="United States of America", plot_width=1200, plot_height=600)

plot.map_options.map_type = "terrain"

source = ColumnDataSource(
    data=dict(
        lat=latitude,
        lon=longitude,
        stars=stars,
        name=business_name,
        fill=color
    )
)

circle = Circle(x="lon", y="lat", size=8, fill_color="fill", line_color="black")
plot.add_glyph(source, circle)

#Map Tools
pan = PanTool()
wheel_zoom = WheelZoomTool()
box_select = BoxSelectTool()
hover_tool = HoverTool()

hover_tool.snap_to_data = True
hover_tool.tooltips = [
    ("Name","@name"),
    ("Rating","@stars")
]

plot.add_tools(pan, wheel_zoom, box_select, hover_tool)

xaxis = LinearAxis(axis_label="lat", major_tick_in=0, formatter=NumeralTickFormatter(format="0.000"))
plot.add_layout(xaxis, 'below')

yaxis = LinearAxis(axis_label="lon", major_tick_in=0, formatter=PrintfTickFormatter(format="%.3f"))
plot.add_layout(yaxis, 'left')

overlay = BoxSelectionOverlay(tool=box_select)
plot.add_layout(overlay)

doc = Document()
doc.add(plot)

filename = "maps.html"
with open(filename, "w") as f:
    f.write(file_html(doc, INLINE, "United States of America"))
#print("Wrote %s" % filename)
view(filename)