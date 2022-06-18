import streamlit as st
import pandas as pd
import numpy as np







def cleanEntries(dataframe):
    # delete entries past last `-- ending hand ${num} --`
    while "ending hand" not in str(dataframe.iloc[0]["entry"]):
        dataframe = dataframe.iloc[1: , :] # drops first row
    

    st.write(dataframe)









st.header("pokernow analyzer")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # To read file as bytes:
    #  bytes_data = uploaded_file.getvalue()
    #  st.write(bytes_data)

    #  # To convert to a string based IO:
    #  stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    #  st.write(stringio)

    #  # To read file as string:
    #  string_data = stringio.read()
    #  st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    #  st.write(dataframe)
    cleanEntries(dataframe)



