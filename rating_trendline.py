__author__ = 'Karthik'
import json
import pandas as pd
from bokeh.plotting import output_file, show, figure
import sys
import matplotlib.pyplot as plt
import datetime

review_dict = {}
date_list = []
stars_list = []
counter = 0
if __name__ == "__main__":

    arg_business_id = sys.argv[1:]
    print arg_business_id

    if len(arg_business_id) == 0:
        print "Please enter the business ID of your place..."
        sys.exit()


    # read the reviews file
    # with open("yelp_academic_dataset_review.json") as f:
    #     for line in f:
    #         json_obj = json.loads(line)
    #
    #         business_id = json_obj.get('business_id')
    #
    #         if business_id == arg_business_id[0]:
    #             stars = json_obj.get('stars')
    #             rev_date = json_obj.get('date')
    #
    #             date_list.append(rev_date)
    #             stars_list.append(stars)
    #
    # review_dict['date'] = date_list
    # review_dict['stars'] = [datetime.datetime.strptime(d,'%Y-%m-%d') for d in date_list]
    # df = pd.DataFrame(review_dict)
    #
    # df.to_csv("rating.csv")

    # The following block will read the data from file as date series and create a data frame.
    df = pd.read_csv("rating.csv",index_col='date',parse_dates=True)
    stars = df['stars']
    ts = pd.TimeSeries(stars)
    # Resample the code to monthly basis and create data
    timeseries_months = ts.resample('M',how='sum')
    # For smooth curve plot interpolate using cubic function
    timeseries_plot = timeseries_months.interpolate(method='linear')
    fig, axis = plt.subplots()
    timeseries_plot.plot(ax=axis)
    fig.savefig("timeseries.png")

    df = pd.read_csv("rating.csv")
    stars_list = df['stars']
    years = pd.DatetimeIndex(df['date']).year

    output_file("trendline.html")
    plot = figure(title="Trendline Example",width=800, height=600)
    plot.line(
        years,
        stars_list,
        x_axis_type = "datetime",
        legend = 'Trendline',
        tools="pan,wheel_zoom,box_zoom,reset,previewsave"
    )

    show(plot)