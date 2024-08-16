from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load the trained model and scaler
model = pickle.load(open('models/best_random_forest_model.pkl', 'rb'))
scaler = pickle.load(open('models/scaler.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        try:
            # Collect user inputs
            data = {
                "MinTemp": [float(request.form['MinTemp'])],
                "MaxTemp": [float(request.form['MaxTemp'])],
                "Rainfall": [float(request.form['Rainfall'])],
                "Evaporation": [float(request.form['Evaporation'])],
                "Sunshine": [float(request.form['Sunshine'])],
                "Humidity9am": [float(request.form['Humidity9am'])],
                "Humidity3pm": [float(request.form['Humidity3pm'])],
                "Pressure9am": [float(request.form['Pressure9am'])],
                "Pressure3pm": [float(request.form['Pressure3pm'])],
                "Temp9am": [float(request.form['Temp9am'])],
                "Temp3pm": [float(request.form['Temp3pm'])],
                "RainToday": [int(request.form['RainToday'])],
                "Season_Autumn": [0],
                "Season_Spring": [0],
                "Season_Summer": [0],
                "Season_Winter": [0]
            }

            # Set season based on selection
            season = request.form['Season']
            data[f'Season_{season}'][0] = 1

            # Create DataFrame
            input_df = pd.DataFrame(data)

            # Scale numerical features
            numerical_columns = ["MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine",
                                 "Humidity9am", "Humidity3pm", "Pressure9am", "Pressure3pm",
                                 "Temp9am", "Temp3pm"]
            input_df[numerical_columns] = scaler.transform(input_df[numerical_columns])

            # Make prediction
            predicted_rainfall = model.predict(input_df)
            prediction = 'Yes' if predicted_rainfall[0] == 1 else 'No'
        except Exception as e:
            print(f"Error occurred: {e}")

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
