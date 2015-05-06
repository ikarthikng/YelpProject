__author__ = 'Karthik'

#All the imports
import json
import nltk
import pickle
import re
import csv
import pandas as pd
from sklearn.cross_validation import train_test_split
import sklearn.metrics as metrics
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

#Declare all the local variables required
scores = {}
user_list = []
business_list = []
review_list = []
csv_list = []

#This function is used to get sentiment score for each word from file
def sentiment_file_scores(filename):
    f = open(filename,"r")

    for line in f:
        word,score = line.split("\t")
        scores[word] = score

#This function is used to get the sentiment score of a string
def calculate_sentiment_score(str):
    total = 0
    words = str.split()

    #Remove all the punctuations and keep only words
    pattern = re.compile('[^A-Za-z]+')
    words = [pattern.sub("",w) for w in words]

    for w in words:
        if w in scores:
            total += int(scores[w])
    return total

#Get all the words in the review string and append it to a list
def get_words_in_reviews(reviews):
    all_words = []
    for (words, sentiment) in reviews:
      all_words.extend(words)
    return all_words

#Get frequency of the words in the string
def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

#This feature set is used by naive bayes classifier to form a training set
def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

#Main function
if __name__ == "__main__":
    # #Read the sentiment scores file and create a dictionary
    sentiment_file_scores("AFINN-111.txt")
    print "Reading training pickle file..."
    #A pickle file is read which is training set for naive bayes classifier
    train_dict = pickle.load(open("train_reviews.p",'rb'))
    #It has two categories. 1. Positive reviews. 2. Negative reviews
    pos_reviews = train_dict['positive']
    neg_reviews = train_dict['negative']

    #Declare the local variables
    reviews = []
    text_temp_list = []
    counter = 0
    pos = 0
    text = ""
    print "Removing words less than 3 letters length and other punctuations..."
    #Remove words with length less or equal to three and also remove all the punctuations
    for (words, sentiment) in pos_reviews + neg_reviews:
        words = re.sub('\W+',' ', words)
        words_filtered = [e.lower() for e in words.split() if len(e) > 3]
        reviews.append((words_filtered, sentiment))

    print "Training the Naives Bayes Classifier..."
    #Train the Naives Bayes Classifier
    word_features = get_word_features(get_words_in_reviews(reviews))
    training_set = nltk.classify.apply_features(document_features, reviews)
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print "Naives Bayes classifier is ready..."
    print "Reading review file and calculating sentiment score for each review..."
    with open("yelp_academic_dataset_review.json") as f:
        for line in f:
            json_obj = json.loads(line)
            try:
                text = json_obj.get('text')
                sent_score = calculate_sentiment_score(text)
                rating = int(json_obj.get('stars'))
                #If the rating is greater than 2.5 and has a sentiment score more than 5, then is considered as positive review else negative
                if rating >= 2.5 and sent_score > 5:
                    pos = 1
                else:
                    pos = 0
                #Append the rating, sentiment score and category as a record to a csv list which is later written to csv file
                csv_list.append((rating, sent_score, pos))
                if counter == 1000:
                    break
                counter += 1
            except ValueError:
                print("Did not find text in the review data...")

    print "Calculating accuracy of Naives Bayes Classifier..."
    print "Accuracy - Naives Bayes Classifier ",nltk.classify.accuracy(classifier, training_set[500:])
    f.close()

    print "Writing rating and sentiment scores of all reviews to csv file..."
    with open("randomForest.csv","wb") as csvfile:
        field_names = ["rating", "sent_score", "category"]
        writer = csv.writer(csvfile)
        writer.writerow(field_names)
        writer.writerows(csv_list)
    csvfile.close()

    print "Reading data from csv file for Random Forest Classifier..."
    data = pd.read_csv("randomForest.csv")
    target = data[['category']]
    train = data[['rating','sent_score']]

    #Principal Component Analysis is used to find the most significant component in the data set and use it for classifier
    pca_estimator = PCA(n_components=1)
    train = pca_estimator.fit_transform(train)

    '''
    ----- Random Forest Classifier -----
    '''
    #Split the data for training and testing the classifier
    x_train, x_test, y_train, y_test = train_test_split(train, target, test_size=0.2, random_state=0)
    #specify a classifier
    clf = RandomForestClassifier(n_estimators=1, criterion='entropy')
    clf.fit(x_train, np.ravel(y_train))
    #let us use the trained classifier to predict the test set
    y_pred = clf.predict(x_test)
    #Test the accuracy of the classifier

    print "Accuracy - Random Forest Classifier ",metrics.accuracy_score(np.ravel(y_test), np.ravel(y_pred))

    '''
    ----- Support Vector Classifier -----
    '''
    x_train, x_test, y_train, y_test = train_test_split(train, target, test_size=0.1, random_state=0)
    #specify a classifier
    clf = SVC(kernel='rbf', probability=True, random_state=33)
    clf.fit(x_train, np.ravel(y_train))
    #let us use the trained classifier to predict the test set
    y_pred = clf.predict(x_test)
    #Test the accuracy of the classifier
    print "Accuracy - SVM classifier",metrics.accuracy_score(np.ravel(y_test), np.ravel(y_pred))

    '''
    ----- Logistic Regression Classifier -----
    '''

    x_train, x_test, y_train, y_test = train_test_split(train, target, test_size=0.1, random_state=0)
    #Prepare the classifier
    clf = LogisticRegression(penalty='l2', dual=True, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=33)
    #perform a fit
    clf.fit(x_train, np.ravel(y_train))
    #Run the prediction score for the test set
    y_pred = clf.predict(x_test)

    print "Accuracy - Logistic Regression ",metrics.accuracy_score(np.ravel(y_test), np.ravel(y_pred))