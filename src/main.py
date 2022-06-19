# from select import select
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from datetime import datetime

import warnings

warnings.filterwarnings("ignore")




# Ex:
# Player stacks: #2 "Dominic @ QXuBqGcQf6" (11.65) | #3 "Lofty @ 7ZqHgUr-OF" (32.45) | #10 "ForesterMike @ uaTX1DrwsW" (25.90)
def graph_player_balance(df, name):

    # filter out player stack events and reverse list
    player_stacks_df = df[df["entry"].str.contains("Player stacks:")][::-1]


    balances = []
    for index, row in player_stacks_df.iterrows():

        if name not in row["entry"]:
            continue

        player_data = row["entry"].replace("Player stacks: ", "").split(" | ")
        
        for d in player_data:
            if name not in d:
                continue

            data = d.split(" ")
            balances.append(round(float(data[-1][1:-1]), 2))

    hands = pd.DataFrame(balances, columns=[f'{name}'])
        
    start = hands.head(1).iloc[0][f'{name}']
    end = hands.tail(1).iloc[0][f'{name}']
    profit = round(end - start, 2)



    # streamlit elements 
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Start", start)
    with col2:
        st.metric("End", end, delta=profit)

    st.line_chart(hands)



def find_unique_players(df):
    player_stacks_df = df[df["entry"].str.contains("Player stacks:")][::-1]
    unique_names = []

    for index, row in player_stacks_df.iterrows():
        player_data = row["entry"].replace("Player stacks: ", "").split(" | ")

        for d in player_data:
            data = d.split(" ")
            name = data[1][1:]

            i = 2
            while data[i] != '@':
                name += " " + data[i]
                i += 1

            name = name.strip()

            if name not in unique_names:
                unique_names.append(name)
    
    return unique_names


def cleanEntries(df):
    # delete entries past last `-- ending hand ${num} --`
    while "ending hand" not in str(df.iloc[0]["entry"]):
        df = df.iloc[1: , :] # drops first row
    
    return df




### STREAMLIT STUFF ###

# elements in sidebar
uploaded_file = st.sidebar.file_uploader(
    "Choose a file",
    type=["csv"]
)

if uploaded_file is not None:
    
    raw_df = pd.read_csv(uploaded_file)
    df = cleanEntries(raw_df)

    unique_players = find_unique_players(df)
    selected_player = st.sidebar.selectbox("Choose player", unique_players)





# main page
if uploaded_file is not None:    

    st.header(f"{selected_player}'s Stats")
    graph_player_balance(df, selected_player)
    


    with st.expander("Raw Data"):
        st.dataframe(raw_df)

else:
    st.header("pokernow analyzer")
