import streamlit as st
import pandas as pd
import numpy as np
import math
from collections import Counter

# Default dataset as a fallback
default_data = {
    'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rainy', 'Rainy', 'Rainy', 'Overcast', 'Sunny', 'Sunny', 'Rainy', 'Sunny', 'Overcast', 'Overcast', 'Rainy'],
    'Temperature': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild', 'Hot', 'Mild'],
    'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'High'],
    'Wind': ['Weak', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Strong'],
    'PlayTennis': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No']
}

# Function to calculate entropy of a list
def entropy_list(a_list):
    cnt = Counter(x for x in a_list)
    num_instance = len(a_list) * 1.0
    probs = [x / num_instance for x in cnt.values()]
    return entropy(probs)

# Function to calculate entropy
def entropy(probs):
    return sum([-prob * math.log(prob, 2) for prob in probs])

# Function to calculate information gain
def info_gain(df, split, target, trace=0):
    df_split = df.groupby(split)
    nobs = len(df.index) * 1.0
    df_agg_ent = df_split.agg({target: [entropy_list, lambda x: len(x) / nobs]})
    df_agg_ent.columns = ['Entropy', 'PropObserved']
    new_entropy = sum(df_agg_ent['Entropy'] * df_agg_ent["PropObserved"])
    old_entropy = entropy_list(df[target])
    return old_entropy - new_entropy

# Function to create an ID3 decision tree
def id3(df, target, attribute_name, default_class=None):
    cnt = Counter(x for x in df[target])
    if len(cnt) == 1:
        return next(iter(cnt))
    elif df.empty or (not attribute_name):
        return default_class
    else:
        default_class = max(cnt.keys())
        gains = [info_gain(df, attr, target) for attr in attribute_name]
        index_max = gains.index(max(gains))
        best_attr = attribute_name[index_max]
        tree = {best_attr: {}}
        remaining_attr = [x for x in attribute_name if x != best_attr]
        for attr_val, data_subset in df.groupby(best_attr):
            subtree = id3(data_subset, target, remaining_attr, default_class)
            tree[best_attr][attr_val] = subtree
        return tree

# Function to classify an instance using the ID3 decision tree
def classify(instance, tree, default=None):
    attribute = next(iter(tree))
    if instance[attribute] in tree[attribute].keys():
        result = tree[attribute][instance[attribute]]
        if isinstance(result, dict):
            return classify(instance, result)
        else:
            return result
    else:
        return default

def main():
    st.title('ID3 Decision Tree Classifier')
    st.write("Upload your training data (CSV file):")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    # Read the uploaded file or use default data
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.DataFrame(default_data)
    
    st.write("Training Data:")
    st.write(data)

    # Extracting attributes and target column
    attributes = list(data.columns)
    target = 'PlayTennis'  # Change if target column name is different
    attributes.remove(target)
    
    # Building the decision tree
    tree = id3(data, target, attributes)
    st.write("\n\nThe Resultant Decision Tree is :")
    st.write(tree)
    
    # Training data and testing data (modify as needed)
    training_data = data.iloc[1:-4]
    test_data = data.iloc[-4:]
    
    train_tree = id3(training_data, target, attributes)
    st.write("\n\nThe Resultant Decision train_tree is :")
    st.write(train_tree)
    
    # Apply classification on the test data
    test_data['predicted2'] = test_data.apply(classify, axis=1, args=(train_tree, 'Yes'))
    st.write("\n\nTesting the model on a few samples and predicting 'PlayTennis' for remaining attributes")
    accuracy = sum(test_data['PlayTennis'] == test_data['predicted2']) / len(test_data.index)
    st.write(f"The accuracy for new trained data is: {accuracy:.2f}")

if __name__ == "__main__":
    main()
