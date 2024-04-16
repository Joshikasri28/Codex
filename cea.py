import numpy as np
import pandas as pd
import streamlit as st
import openpyxl

st.title("Candidate Elimination Algorithm")

# Function to perform the Candidate Elimination Algorithm
def learn(concepts, target):
    specific_h = concepts[0].copy()
    general_h = [["?" for _ in range(len(specific_h))] for _ in range(len(specific_h))]

    for i, h in enumerate(concepts):
        if target[i] == "yes":
            for x in range(len(specific_h)):
                if h[x] != specific_h[x]:
                    specific_h[x] = '?'
                    general_h[x][x] = '?'
        elif target[i] == "no":
            for x in range(len(specific_h)):
                if h[x] != specific_h[x]:
                    general_h[x][x] = specific_h[x]
                else:
                    general_h[x][x] = '?'

    indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]
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
