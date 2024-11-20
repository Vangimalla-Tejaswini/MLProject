from flask import Flask,request,render_template
import numpy as np
import pickle
import os
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipelines.prediction_pipeline import CustomData,PredictPipeline

application = Flask(__name__)  # Create the Flask application
app = application 

# Load the model from the artifacts folder
current_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory of the script
model_path = os.path.join(current_dir, 'artifacts', 'model.pkl')  # Path to model.pkl
with open(model_path, 'rb') as f:
    model = pickle.load(f)

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))

        )
        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction")

        predict_pipeline=PredictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)
        print("after Prediction")
        return render_template('home.html',results=results[0])
    

if __name__=="__main__":
    app.run(host="0.0.0.0")        
    
    
    
    