import streamlit as st
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Function to load data
@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/your_username/your_repository/main/tennisdata.csv"
    data = pd.read_csv(url)
    return data

# Load data
data = load_data()

# Preprocess data
X = data[['Outlook', 'Temperature', 'Humidity', 'Windy']]
y = data['PlayTennis']
le = LabelEncoder()
X['Outlook'] = le.fit_transform(X['Outlook'])
X['Windy'] = le.fit_transform(X['Windy'])
y = le.fit_transform(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train classifier
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Streamlit app
st.title("Tennis Prediction App")
st.write("This app predicts whether you should play tennis based on weather conditions.")

# User input
outlook = st.selectbox("Outlook", ['Sunny', 'Overcast', 'Rainy'])
temperature = st.slider("Temperature", min_value=0, max_value=100, value=50, step=1)
humidity = st.slider("Humidity", min_value=0, max_value=100, value=50, step=1)
windy = st.radio("Windy", ['False', 'True'])

# Convert user input to appropriate format
outlook = le.transform([outlook])[0]
windy = le.transform([windy])[0]

# Make prediction
prediction = classifier.predict([[outlook, temperature, humidity, windy]])
prediction = le.inverse_transform(prediction)[0]

# Display prediction
st.write("Prediction:", prediction)
