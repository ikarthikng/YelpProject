# YelpProject
Yelp project for data science class INSY 5378

 
Table of Contents
1.	Introduction	2
2.	Objective	4
3.	Dataset description	9
3.1	Data Preprocessing/Data cleaning	10
3.2	Predictive attributes	11
3.3	Class attributes	12
4.	Working	4
5.	Analysis of results	4
6.	Data Visualization 	9












Introduction 
Data was obtained from Yelp official website which is made available for academic purpose.
We could access the Yelp Dataset, which is governed by the separate Dataset Challenge Academic

Yelp connects people to great local businesses. To help people find great local businesses, Yelp engineers have developed an excellent search engine to sift through over 61 million reviews and help people find the most relevant businesses for their everyday needs. The Yelp Dataset Challenge began in Feb 5, 2015 and continues through June 30, 2015 

Contest is open only to undergraduate and graduate university students in countries not restricted by the Office of Foreign Assets Control of the United States Department of the Treasury. Participants must be 18 or older and currently enrolled in an accredited degree program in any field.

Objective
The objective is to present the impact of rating, reviews and check-in’s by customers on business. This can help business improve based on the analysis done such parameters.
Using all the techniques taught in data science, we tried to apply most of it to this project where we try to predict a review is negative or positive by analysing the words and sentiment score of the review.
Data visualization is implemented to comprehend and understand the pattern of the data in a better just by looking a chart or a map. This will save time and understand a business’s position over time in a particular region.


Dataset Description
The dataset is a single gzip-compressed file, composed of one json-object per line. Every object contains a 'type' field, which tells you whether it is a business, a user, or a review.
Business Objects
Business objects contain basic information about local businesses. The 'business_id' field can be used with the Yelp API to fetch even more information for visualizations, but note that you'll still need to comply with the API TOS. The fields are as follows: 
{
  'type': 'business',
  'business_id': (a unique identifier for this business),
  'name': (the full business name),
  'neighborhoods': (a list of neighborhood names, might be empty),
  'full_address': (localized address),
  'city': (city),
  'state': (state),
  'latitude': (latitude),
  'longitude': (longitude),
  'stars': (star rating, rounded to half-stars),
  'review_count': (review count),
  'photo_url': (photo url),
  'categories': [(localized category names)]
  'open': (is the business still open for business?),
  'schools': (nearby universities),
  'url': (yelp url)
}

Review Objects
Review objects contain the review text, the star rating, and information on votes Yelp users have cast on the review. Use user_id to associate this review with others by the same user. Use business_id to associate this review with others of the same business.
{
  'type': 'review',
  'business_id': (the identifier of the reviewed business),
  'user_id': (the identifier of the authoring user),
  'stars': (star rating, integer 1-5),
  'text': (review text),
  'date': (date, formatted like '2011-04-19'),
  'votes': {
    'useful': (count of useful votes),
    'funny': (count of funny votes),
    'cool': (count of cool votes)
  }
}

User Objects
User objects contain aggregate information about a single user across all of Yelp (including businesses and reviews not in this dataset).
{
  'type': 'user',
  'user_id': (unique user identifier),
  'name': (first name, last initial, like 'Matt J.'),
  'review_count': (review count),
  'average_stars': (floating point average, like 4.31),
  'votes': {
    'useful': (count of useful votes across all reviews),
    'funny': (count of funny votes across all reviews),
    'cool': (count of cool votes across all reviews)
  }
}

Data Prepossessing
Data prepossessing is one of the most important steps in data science. If there is much irrelevant and redundant information present in the data, we can remove it with the help of data prepossessing steps. Data prepossessing steps include data cleaning, normalization, transformation, feature extraction, etc. Following steps were carried out in our project.
1.	Stop words, punctuations, digits and special characters are removed from the reviews
2.	The words in reviews whose length is less than three characters are not considered.
3.	Two lists are created one for negative reviews and the other for positive reviews for training Naives Bayes classifier.
4.	If a rating is less than 2.5 on a review for a business and its sentiment score is less than 5, review is considered as negative and if the rating is greater than or equal to 2.5 and sentiment score is greater than 5 then review is considered as positive.

Predictive Attributes
Predictive attributes are attributes which add value or meaning to the data and is useful in prediction of the class attribute. In this part of the project we tried to predict whether a review is emotionally negative or positive using certain classifiers.
Working
Two pickle files are created. One for training set for Naïve Bayes classifier and other for extracting the business names from the business IDs. Four classifiers are used. 
One from NLTK package: Naïve Bayes:
•	Naïve Bayes uses only string data type to work and make predictions. 
•	Training set is created from the data and based on the predictions done on it by the classifier, accuracy is obtained.
Three classifiers are taken from the SKLEARN package: 
1.	RandomForest Classifier
2.	LogisticRegression Classifier
3.	SVM Classifier
Sentiment Analysis is implemented for making predictions and obtaining accuracy for these classifiers because the classifiers from the SKLEARN package can work only with numeric data for class attribute.
Sentimental scores are calculated for each review using the AFINN.txt file and category value 1 is assigned to good review and 0 for a bad review. The value for rating, sentimental score and category is returned as tuple and predictions and accuracies are calculated likewise.



Accuracies obtained from classifiers:
 
Accuracies changes each time when we run the program because the sklearn uses cross validation and split and test functionalities. Therefore, above results are subject to change when the program is executed is next time. 
Analysis of Results:
Naïve Bayes classifier takes a long time to run before it has to process each and every string which is computationally expensive and also it creates a load on the memory. As we can see from the accuracy results, Naïve Bayes mostly depends on the training set to create the classifier. Therefore, accuracy is also determined accordingly. The advantage of Naïve Bayes classifier over other classifiers is that it can used directly on the string set and it need not converted to any numerical format which is required in the other classifiers.
Other classifier except the data to be numerical format, therefore two columns were created. First column, contained ratings given by the users and second column had sentiment scores calculated in the previous step. This data is written to csv file and later on using pandas we read the same csv file and create train and test sets using cross validation of sklearn. 
This step is common to all the classifier. Some parameters we changed and tested each time to improve the accuracy of the classifier. The code base has some parameters which will give the best accuracy of the classifiers. 
As we can see from the results, random forest classifier is the best classifier amongst all with the highest accuracy results and was able to predict whether the string is positive or negative more accurately than other classifiers.














Data Visualization
Visual representation of the data is better in most cases because it helps to understand the data, pattern and predict certain without looking at the millions of records at the same time. We have implemented three programs which helps to visual the 1.5 million record and help the business in a better way.
Visual 1
We wanted to mine as much data as possible. Our dataset includes social data where customers have checked in at the business establishment at certain time and certain day of the week. 
First Attempt
We wanted to visualize which part of the day and week were customers more socially active at a business establishment at a particular area but the data is sparse and most of the business establishment does not have any data. Therefore we had to improvise.
Second Attempt
We compiled the whole and wanted to check which business place was most socially active. Therefore we process the entire data and checked the top 10 socially active places and created a bar chart using the results. The result is as shown in the below picture.  
 
X-Axis represents the business establishment and y-axis gives the total number of checkin at that particular establishment. The above chart was created a visual python library called bokeh which internally uses a javascript library called d3js
Visual 2
The business objective behind second visual program was to have a chart or a tool which will give the progress of the establishment over the years based on the ratings given by the customers who visited the place. This idea led to creating a rating trend line which is plotted for the entire data in the dataset.


 
First Attempt
This attempt also used bokeh library which gave the result as shown in the below picture. The picture shows all the ratings over the years which from the processed data. 
 
Second Attempt
The plot was not good and it was too “spiky” for a visual chart. We normalized the data using pandas time series. Using interpolation (filled the data between the years using mathematical formula, in this case a cubic function), we were able to create a chart which was much more meaning than the first attempt which is as shown in the below picture. This was done using pandas time series and matlibplot. 
 
Visual 3
Suppose there is food chain which has thousands of restaurants all over the country. We wanted to create a visual map where we can see all the chains and their ratings based on color code. This help in visualizing and helping senior management to decide which region or business place to concentrate when the rating is low. Depending on the rating given to the place we were able to create a map where all the business places were plotted and given a color code
1.	Rating 4 to 5 is green
2.	Rating 3 to 4 is yellow
3.	Rating 2 to 3 is orange
4.	Rating 1 to 2 is red
 
This visual map was also created using bokeh library.
Code Base
https://github.com/karthikfamilyn/YelpProject




