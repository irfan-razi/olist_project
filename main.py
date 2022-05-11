from flask import Flask, render_template, request, Response
import pickle
import numpy as np
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
from wsgiref import simple_server
import os

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/prediction", methods=['POST'])
@cross_origin()
def prediction():
    try:
        if request.method == 'POST':

            # Get the data from the POST request.
            order_qty = request.form['order_qty']
            product_weight = request.form['product_weight']
            payment_installments = request.form["payment_installments"]
            order_delivered_customer_time_in_days = request.form["order_delivered_customer_time_in_days"]
            product_volume = request.form["product_volume"]
            customer_seller_distance = request.form["customer_seller_distance"]
            order_purchase_year = request.form["order_purchase_year"]
            total_payment = request.form["total_payment"]
            order_status_encoded = request.form["order_status_encoded"]
            payment_type_encoded = request.form["payment_type_encoded"]
            product_category_name_english_encoded = request.form["product_category_name_english_encoded"]
            timing_encoded = request.form["timing_encoded"]
            Seasons_encoded = request.form["Seasons_encoded"]


            # Convert the data into numpy array
            input = np.array([[order_qty, product_weight, payment_installments,
                            order_delivered_customer_time_in_days, product_volume, customer_seller_distance,
                            order_purchase_year, total_payment, order_status_encoded, payment_type_encoded,
                            product_category_name_english_encoded, timing_encoded, Seasons_encoded]])

            # Load the model from the pickle file
            model = pickle.load(open("model/model.pkl", 'rb'))

            # Make the prediction
            prediction = model.predict(input)

        return render_template('predict.html',data=prediction)

    except Exception as e:
        return Response("Error Occurred! %s" %e)
 

port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    # port = 5000
    httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    httpd.serve_forever()