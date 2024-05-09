import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd

def load_data():
    filename = filedialog.askopenfilename()
    data = pd.read_csv(filename)
    concepts = np.array(data.iloc[:, 0:-1])
    target = np.array(data.iloc[:, -1])
    return concepts, target

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

def run_algorithm():
    concepts, target = load_data()
    s_final, g_final = learn(concepts, target)
    s_final_label.config(text="Final Specific_h:\n" + str(s_final))
    g_final_label.config(text="Final General_h:\n" + str(g_final))

# Creating UI
root = tk.Tk()
root.title("Candidate Elimination Algorithm")
root.geometry("400x300")

load_button = tk.Button(root, text="Load Data", command=run_algorithm)
load_button.pack(pady=10)

s_final_label = tk.Label(root, text="Final Specific_h:\n")
s_final_label.pack(pady=5)

g_final_label = tk.Label(root, text="Final General_h:\n")
g_final_label.pack(pady=5)

root.mainloop()
