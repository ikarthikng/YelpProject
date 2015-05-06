'''
Read checkin file to find the busiest hour of the business and plot a graph for a business
'''
import json
import pickle
from bokeh.charts import Bar
from bokeh.plotting import output_file, show
import operator

def createPickleForBusiness():
    business_dict = {}
    #read the business file
    with open("yelp_academic_dataset_business.json") as f:
        for line in f:
            json_obj = json.loads(line)
            business_id = json_obj.get('business_id')
            business_name = json_obj.get('name')
            business_dict[business_id] = business_name

    print business_dict
    pickle.dump(business_dict,open("business_details.p",'wb'))

if __name__ == "__main__":
    #createPickleForBusiness() -- Call this function only when necessary
    #read the checkin file
    checkin_dict = {}
    business_dict = pickle.load(open("business_details.p","rb"))
    with open("yelp_academic_dataset_checkin.json") as file_checkin:
        for line in file_checkin:
            json_obj = json.loads(line)

            checkin_info = json_obj.get('checkin_info')
            business_id = json_obj.get('business_id')
            counter = 0
            for key, value in checkin_info.iteritems():
                counter = counter + 1
            if business_id in checkin_dict:
                count = checkin_dict.get(business_id)
                count = count + counter
                checkin_dict[business_id] = count
            else:
                checkin_dict[business_id] = counter
            counter = 0

    sorted_checkin = sorted(checkin_dict.items(), key=operator.itemgetter(1),reverse=True)
    ids = []
    counts = []
    for key,value in sorted_checkin:
        if key in business_dict:
            name = business_dict.get(key)
        ids.append(name)
        counts.append(value)


    output_file('checkin.html')

    # create a figure()
    bar = Bar(counts[:10],ids[:10], title="Checkin Information", width=1024, height=768)
    show(bar)