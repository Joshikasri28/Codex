import streamlit as st
import numpy as np
import pandas as pd

def learn(concepts, target):
    specific_h = concepts[0].copy()
    general_h = [["?" for _ in range(len(specific_h))] for _ in range(len(specific_h))]
    for i, h in enumerate(concepts):
        if target[i] == "yes":
            for x in range(len(specific_h)):
                if h[x] != specific_h[x]:
                    specific_h[x] = '?'
                    general_h[x] = '?'
        if target[i] == "no":
            for x in range(len(specific_h)):
                if h[x] != specific_h[x]:
                    general_h[x][x] = specific_h[x]
                else:
                    general_h[x][x] = '?'
    indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]
    for i in indices:
        general_h.remove(['?', '?', '?', '?', '?', '?'])
    return specific_h, general_h

def run_algorithm(data_file):
    data = pd.read_csv(data_file)
    concepts = np.array(data.iloc[:, 0:-1])
    target = np.array(data.iloc[:, -1])
    s_final, g_final = learn(concepts, target)
    return s_final, g_final

st.title("Candidate Elimination Algorithm")

uploaded_file = st.file_uploader("Upload CSV file", type="csv")
if uploaded_file is not None:
    s_final, g_final = run_algorithm(uploaded_file)
    st.subheader("Final Specific_h:")
    st.write(s_final)
    st.subheader("Final General_h:")
    st.write(g_final)
