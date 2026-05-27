import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

### read excel
def read_excel(file):
    df = pd.read_excel(file)
    return df
df=pd.read_excel(r'data\sales.xls')
st.title('Sales Data Analysis')
st.write('This is a simple Streamlit app to ' \
'analyze sales data.')
st.write("shape of the dataset")
st.write(df.shape)
st.dataframe(df.head())