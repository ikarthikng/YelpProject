__author__ = 'Karthik'
"""
This program is used to generate the pickle files necessary for the project
-> This program will take some time to run because it has to scan all the big files. Please be patient
"""
import pickle
import json

def create_pickle_for_reviews():
    train_dict = {}
    neg_reviews = []
    neg_counter = 0
    pos_reviews = []
    pos_counter = 0
    with open("yelp_academic_dataset_review.json") as review_file:
        for line in review_file:
            json_obj = json.loads(line)
            text = json_obj.get('text')
            """
            -> Any review with less than or equal to 2.5 stars is assumed to be negative review
            -> Any review with greater than 2.5 stars is assumed to be positive review
            These are just the assumptions made based on a model.
            """
            if json_obj.get('stars') <= 2.5 and neg_counter < 500:
                temp = (text, 'neg')
                neg_reviews.append(temp)
                neg_counter += 1
            elif json_obj.get('stars') > 2.5 and pos_counter < 500:
                temp = (text, 'pos')
                pos_reviews.append(temp)
                pos_counter += 1
            """
            -> As of now the limit of two lists of positive and negative reviews are 1000 records each. If necessary, please change it below
            """
            if pos_counter >= 1000 and neg_counter >= 1000:
                break

        train_dict['positive'] = pos_reviews
        train_dict['negative'] = neg_reviews
        pickle.dump(train_dict, open("train_reviews.p", 'wb'))

        review_file.close()

def create_pickle_for_business():
    business_dict = {}
    with open("yelp_academic_dataset_business.json") as business_file:
        for line in business_file:
            json_obj = json.loads(line)
            business_id = json_obj.get('business_id')
            business_name = json_obj.get('name')
            business_dict[business_id] = business_name

    pickle.dump(business_dict,open("business_details.p",'wb'))
    business_file.close()


if __name__ == "__main__":
    #Create necessary pickle files
    create_pickle_for_reviews()
    create_pickle_for_business()