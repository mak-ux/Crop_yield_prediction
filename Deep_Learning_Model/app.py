from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
#from flask import Flask, render_template, request
from sklearn.externals import joblib
import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras
app = Flask(__name__)

#mul_reg = open("multiple_regression_model.pkl", "rb")
#ml_model = joblib.load(mul_reg)
ml_model = keras.models.load_model("my_Func_model.h5")

#app = Flask(__name__)

#mul_reg = open("multiple_regression_model.pkl", "rb")
#ml_model = joblib.load(mul_reg)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Kanhaiya', password='password'))
users.append(User(id=2, username='Kanhaiya', password='password'))
users.append(User(id=3, username='Kanhaiya', password='password'))


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        
@app.route("/")
def front():
	return render_template('front.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('home.html')
    
@app.route('/home')
def home():
    if not g.user:
        return redirect(url_for('login'))

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

        
if __name__ == '__main__':
    app.run(debug=True)
    
