import streamlit as st
import pandas as pd
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Load the data
@st.cache
def load_data():
    data = pd.read_csv("https://raw.githubusercontent.com/your_username/your_repository/main/tennisdata.csv")
    return data

data_load_state = st.text("Loading data...")
data = load_data()
data_load_state.text("Data loaded successfully!")

# Preprocess the data
X = data.iloc[:,:-1]
y = data.iloc[:,-1]
le_outlook = LabelEncoder()
X.Outlook = le_outlook.fit_transform(X.Outlook)
le_Temperature = LabelEncoder()
X.Temperature = le_Temperature.fit_transform(X.Temperature)
le_Humidity = LabelEncoder()
X.Humidity = le_Humidity.fit_transform(X.Humidity)
le_Windy = LabelEncoder()
X.Windy = le_Windy.fit_transform(X.Windy)
le_PlayTennis = LabelEncoder()
y = le_PlayTennis.fit_transform(y)

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.20)

# Train the classifier
classifier = GaussianNB()
classifier.fit(X_train,y_train)

# Create the Streamlit app
def main():
    st.title("Tennis Prediction App")
    st.write("This app predicts whether you should play tennis based on weather conditions.")
    
    # Collect user input
    outlook = st.selectbox("Outlook", ["Sunny", "Overcast", "Rainy"])
    temperature = st.slider("Temperature", min(X.Temperature), max(X.Temperature), step=1)
    humidity = st.slider("Humidity", min(X.Humidity), max(X.Humidity), step=1)
    windy = st.selectbox("Windy", ["False", "True"])
    
    # Convert user input to appropriate format
    outlook = le_outlook.transform([outlook])[0]
    windy = le_Windy.transform([windy])[0]
    
    # Make prediction
    prediction = classifier.predict([[outlook, temperature, humidity, windy]])
    prediction = le_PlayTennis.inverse_transform(prediction)[0]
    
    # Display prediction
    st.write("Prediction:", prediction)

if __name__ == "__main__":
    main()
