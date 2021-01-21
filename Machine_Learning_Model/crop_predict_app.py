from flask import Flask, render_template, request
from sklearn.externals import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

mul_reg = open("multiple_regression_model.pkl", "rb")
ml_model = joblib.load(mul_reg)


@app.route("/")
def home():
	return render_template('home.html')

@app.route("/predict", methods=['POST'])
def predict():
	try:
		Lattitude= float(request.form['Latitude'])
		Longitude= float(request.form['Longitude'])
            
		ATMAX = float(request.form['ATMAX'])
		ATMIN = float(request.form['ATMIN'])
		humidity = float(request.form['humidity'])
		pressure = float(request.form['pressure'])
		tempmax = float(request.form['tempmax'])
		tempmin = float(request.form['tempmin'])
		pred_args = [Lattitude,Longitude,ATMAX, ATMIN,humidity, pressure, tempmax,tempmin]
		pred_args_arr = np.array(pred_args)
		pred_args_arr = pred_args_arr.reshape(1, -1)
            
		model_prediction = ml_model.predict(pred_args_arr)
		model_prediction = round(float(model_prediction), 2)
	except ValueError:
		return "Please check if the values are entered correctly"
	return render_template('predict.html', prediction = model_prediction)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
