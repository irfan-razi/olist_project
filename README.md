# Market Basket Project on E-Commerce
With population size of 138 crores, India is the seventh largest country by area, the second most populous country, and the most populous democracy in the world So, we have a resource which no other country is able to match, which is human resource With the development of the technology, ease of online services, UPI transactions, India is way ahead than any other country Competition among the vendors are high They are working really hard to make the service as good as possible In such cases feedbacks and reviews play a major role.

Most customers do not post a review rating or any comment after purchasing a product which is a challenge for any E commerce platform to perform If a company predicts whether a customer liked/disliked a product so that they can recommend more similar and related products as well as they can decide whether or not a product should be sold at their end This is crucial for E commerce based company because they need to keep track of each product of each seller, so that none of products discourage their customers to come shop with them again Moreover, if a specific product has very few ratings and that too negative, a company must not drop the product straight away, may be many customers who found the product to be useful haven't actually rated it Some reasons could possibly be comparing your product review with those of your competitors beforehand, gaining lots of insight about the product and saving a lot of manual data pre processing, maintain good customer relationship with company, lend gifts, offers and deals if the company feels the customer is going to break the relation.

# About Dataset
### Brazilian E-Commerce Public Dataset by Olist
This is a Brazilian ecommerce public dataset of orders made at Olist Store. The dataset has information of 100k orders from 2016 to 2018 made at multiple marketplaces in Brazil. Its features allows viewing an order from multiple dimensions: from order status, price, payment and freight performance to customer location, product attributes and finally reviews written by customers. We also released a geolocation dataset that relates Brazilian zip codes to lat/lng coordinates.

This is real commercial data, it has been anonymised, and references to the companies and partners in the review text have been replaced with the names of Game of Thrones great houses.

### Context
This dataset was generously provided by Olist, the largest department store in Brazilian marketplaces. Olist connects small businesses from all over Brazil to channels without hassle and with a single contract. Those merchants are able to sell their products through the Olist Store and ship them directly to the customers using Olist logistics partners.

After a customer purchases the product from Olist Store a seller gets notified to fulfill that order. Once the customer receives the product, or the estimated delivery date is due, the customer gets a satisfaction survey by email where he can give a note for the purchase experience and write down some comments.

### Notes
- An order might have multiple items.
- Each item might be fulfilled by a distinct seller.
- All text identifying stores and partners where replaced by the names of Game of Thrones great houses.

# Data Schema
The data is divided in multiple datasets for better understanding and organization. Please refer to the following data schema when working with it:

![data_schema](https://user-images.githubusercontent.com/41921480/163558145-f8f8c781-0f76-4ae3-b80d-36343f4cfdcc.png)


Brazilian E-Commerce Public Dataset by Olist:
url: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

## EDA
(url: https://github.com/irfan-razi/olistproject/blob/main/EDA/EDA.ipynb)

There have been quite few observations:

1. Online shopping has increased drastically since 2017.
![07_shoppingtrend](https://user-images.githubusercontent.com/41921480/163558882-484f3114-6a03-474f-a35d-42c8bd1a2af2.png)

2. We can notice that August and May are the months with maximum orders.
![08_shoppingtrend_mont](https://user-images.githubusercontent.com/41921480/163559037-7b1dc093-84f7-43fa-9976-ee3d1ef0b384.png)

3. Shopping time is highest around 4pm, 2pm and 11am.
![09_shoppingtime](https://user-images.githubusercontent.com/41921480/163559125-82f00ee4-6fd6-4de4-85a7-ac8d4d37eec7.png)

4. Customer Segmentation City-Wise
![10_customerreview](https://user-images.githubusercontent.com/41921480/163559200-5cd3eeb6-209c-4a66-9482-10efc66b52d6.png)

## Approach

1. **Data Description:** We will be using Brazilian E-Commerce Public Dataset by Olist. This is a Brazilian ecommerce public dataset of orders made at Olist Store. The dataset has information of 100k orders from 2016 to 2018 made at multiple marketplaces in Brazil. Its features allow viewing an order from multiple dimensions: from order status, price, payment and freight performance to customer location, product attributes and finally reviews written by customers. We also released a geolocation dataset that relates Brazilian zip codes to lat/lng coordinates.

2. **Data Ingestion:** Here, we will be ingesting all the batches of data from Cassandra database to our machine in csv format.

3. **Data Pre-processing:** We will do Exploratory Data Analysis of the data in Jupyter Notebook to get the complete understanding of the data. Based on that we can decide the strategy for Data Processing and validation. We may have to drop insignificant columns, handle missing values, handle imbalanced data, etc so that we can get a clean data for model training. For this, we have to write separate modules as per our need.

4. **Model Training:** We train our data with various ML models. Among those, Random Forest Classifier is the best fit model.

5. **Model Evaluation:** Model evaluation is done by classification report. Since, this is a problem of imbalanced data, we have to analyse and improve Recall score and F1-score, not just Accuracy.

6. **Model Saving:** After model training and evaluation, we will save the model for production.

7. **Model Push to WebApp:** We are going to do the cloud setup for our model deployment. We are going to create Flask App and User Interface. We will integrate our model with it.

8. **Data from client for Testing:** Now, our Web-Application is ready and deployed to clouds. We can get the data from our clients and start testing the model. Client-data is also required to go through the same process as our train data has gone for model training.

9. **Prediction:** Finally, when we complete the prediction process with client’s data, we convert it into csv format and share it to the client.


## Web Deployment
•	Heroku is used for model deployment.
•	Docker hub is used for Dockerization.
•	Circleci is used for CI-CD pipeline.

## Tools used
![tools](https://user-images.githubusercontent.com/41921480/163561984-47c48847-c01b-4685-bfc0-a3f4fb6ae577.png)

## User Interface for WebApp
![01](https://user-images.githubusercontent.com/41921480/163562159-07fadcf4-b473-479e-b223-3bb2cebe9ea5.png)
![02](https://user-images.githubusercontent.com/41921480/163562166-6875b138-17fb-46c0-a8f0-6cb2f19f0911.png)


## Project Documents

1. [Architecture Document](https://github.com/irfan-razi/olistproject/blob/main/docs/Architecture.pdf)
2. [Low Level Design Document](https://github.com/irfan-razi/olistproject/blob/main/docs/LLD.pdf)
3. [High Level Design Document](https://github.com/irfan-razi/olistproject/blob/main/docs/HLD.pdf)
4. [Detailed Project Report](https://github.com/irfan-razi/olistproject/blob/main/docs/DPR.pdf)
5. [Wireframe Document](https://github.com/irfan-razi/olistproject/blob/main/docs/Wireframe.pdf)

## Demo Video

https://user-images.githubusercontent.com/41921480/163562961-1f8feb4a-a8fd-47a7-9c63-d7dbee798e18.mp4


## Author

Irfan Razi [LinkedIn](https://www.linkedin.com/in/irfan-razi-a4a633156/)
