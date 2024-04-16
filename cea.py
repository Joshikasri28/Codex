import streamlit as st
import numpy as np
import pandas as pd

def learn(concepts, target):
    specific_h = concepts[0].copy()
    general_h = [["?" for _ in range(len(specific_h))] for _ in range(len(specific_h))]

    for i, h in enumerate(concepts):
        if target[i] == "Yes":
            for x in range(len(specific_h)):
                if h[x] != specific_h[x]:
                    specific_h[x] = '?'
                    general_h[x][x] = '?'
        if target[i] == "No":
            for x in range(len(specific_h)):
                if h[x] != specific_h[x]:
                    general_h[x][x] = specific_h[x]
                else:
                    general_h[x][x] = '?'

    indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]
    for i in indices:
        general_h.remove(['?', '?', '?', '?', '?', '?'])
    return specific_h, general_h

def main():
    st.title('Candidate Elimination Algorithm')
    st.write("Upload your training data (CSV file):")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    # Define a default dataset in case no file is uploaded
    default_data = {
        'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rainy', 'Rainy', 'Rainy', 'Overcast', 'Sunny', 'Sunny', 'Rainy', 'Sunny', 'Overcast', 'Overcast', 'Rainy'],
        'Temperature': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild', 'Hot', 'Mild'],
        'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'High'],
        'Wind': ['Weak', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Strong'],
        'Play': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No']
    }
    
    # Read the uploaded file or use default data
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.DataFrame(default_data)
    
    st.write("Training Data:")
    st.write(data)

    concepts = np.array(data.iloc[:, 0:-1])
    target = np.array(data.iloc[:, -1])
    
    s_final, g_final = learn(concepts, target)
    st.write("Final Specific_h:")
    st.write(s_final)
    st.write("Final General_h:")
    st.write(g_final)

if __name__ == "__main__":
    main()
    for i in indices:
        general_h.remove(['?', '?', '?', '?', '?', '?'])

    return specific_h, general_h

# File upload and processing
uploaded_file = st.file_uploader("Upload a dataset (Excel format)", type=["xlsx"])

if uploaded_file is not None:
    try:
        data = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully.")
        concepts = data.iloc[:, 0:-1].values
        target = data.iloc[:, -1].values

        s_final, g_final = learn(concepts, target)

        # Display results
        st.write("Final Specific_h:", s_final)
        st.write("Final General_h:", g_final)

    except Exception as e:
        st.error(f"An error occurred: {e}")
