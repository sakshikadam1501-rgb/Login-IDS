from flask import Flask, render_template, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import sqlite3


app = Flask(__name__)

# Load dataset
data = pd.read_csv("login_data.csv")

# Encode label
le = LabelEncoder()
data['label'] = le.fit_transform(data['label'])

# Features & label
X = data[['ip', 'login_time', 'failed_attempts']]
y = data['label']

# Train model
model = RandomForestClassifier()
model.fit(X, y)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    ip = int(request.form['ip'])
    time = int(request.form['login_time'])
    failed = int(request.form['failed_attempts'])

    # Rule-based logic
    if failed > 5:
        result = "🚨 Intruder Detected! (Too many failed attempts)"
    else:
        user_input = pd.DataFrame([[ip, time, failed]],
                                 columns=['ip', 'login_time', 'failed_attempts'])
        prediction = model.predict(user_input)

        if prediction[0] == 0:
            result = "🚨 Intruder Detected!"
        else:
            result = "✅ Normal User"

    return render_template('index.html', prediction_text=result)




if __name__ == "__main__":
    app.run(debug=True)