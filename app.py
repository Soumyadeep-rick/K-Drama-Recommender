import joblib
import pandas as pd
import streamlit as st 
from scipy import spatial

st.title("S&V's") 
st.header("K-Drama Recommender")
st.sidebar.header("About")
st.sidebar.markdown("This website allows you to get K-Drama recommendation of your choice.")
st.sidebar.subheader("Made By")
st.sidebar.info("Soumyadeep")
st.sidebar.success("Vaishnavi")
st.sidebar.subheader("Special Thanks To")
st.sidebar.warning("Shreyansh")

df = pd.read_csv('DatasetK.csv')
df= df.dropna(how='any', axis=0)
df.reset_index(drop=True, inplace=True)
df3 = df.copy()
df1 = df.drop(columns=['Year of release', 'Number of Episode', 'Duration/min', 'Rank', 'Network', 'Content Rating'], axis=1)
df1['Rating'] = df1['Rating']/10
df1 = df1.drop(columns=['First Aired','Last Aired','Air Day 1_Saturday','Air Day 1_Sunday','Air Day 1_Wednesday', 'Air Day 2_Saturday', 'Air Day 2_Sunday', 'Air Day 2_Thursday', 'Air Day 2_Tuesday', 'Air Day 3_Wednesday', 'Air Day 1_Friday',	'Air Day 1_Monday',	'Air Day 1_Thursday',	'Air Day 1_Tuesday'], axis=1)
name = df1[['Name']]
name = name.head(10)
df2 = df1.drop(columns=['Name'],axis = 1)

@st.cache()
def recm(name, n):
    idx = df1[df1['Name'] == name].index[0]
    dist = pd.DataFrame(data = df2.index)
    dist = dist[dist[0] != idx]
    dist['distance'] = dist[0].apply(lambda x: spatial.distance.euclidean(df2.loc[x],df2.loc[idx]))
    dist.sort_values(by='distance' , inplace= True)
    dist.drop(columns = [0],axis =1 , inplace=True)
    return dist.head(n)

opt = st.selectbox("Choose a K-Drama", df['Name'])
no = st.slider('Select No. of Recommendations', 1, 10, 3)
if(st.button("Get Recommendation")):
    x = recm(opt, no)
    df4 = pd.merge(df3, x, left_index=True, right_index=True)
    df4.sort_values(by='distance' , inplace= True)
    df4.reset_index(drop=True, inplace=True)
    df4 = df4[['Name', 'Year of release', 'Network', 'Rating']]
    df4.index = df4.index + 1
    st.table(df4)