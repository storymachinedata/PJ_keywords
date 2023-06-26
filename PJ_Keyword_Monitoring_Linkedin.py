
import streamlit as st
import datetime as dt
from helpers import *



st.set_page_config(layout='wide')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# logo, _ = st.columns(2)
# with logo:
# 	st.image(storymch_logo, width=200)
   
st.markdown("<h1 style='text-align: center; color: green;'>PJ Linkedin posts from Keywords</h1>", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)

with col1:
	filter_day = st.number_input("How many days older posts?", min_value=1, max_value=100, value=7, step=1)
	if filter_day:
		st.success(f'Showing Posts from last {int(filter_day)} Days', icon="✅")

with col2:
	filter_Interactions = st.selectbox( "Filter by total interactions",
						('Total Interaction: High to Low',
						'Total Interaction: Low to High'))

with col3:
	filter_date = st.selectbox( "Filter by total Post date",
						('Posts: Newest First',
						'Posts: Oldest First'))


kath_brienne_path = 'https://cache1.phantombooster.com/UhrenaxfEnY/X2E7Q7Stb706drcvRA3MKA/pj_6_26.csv'



kath_brienne_main = read_file(kath_brienne_path)
kath_brienne_df = kath_brienne_main[kath_brienne_main['date']>=(dt.datetime.now()-dt.timedelta(days=filter_day))]
kath_brienne_df = kath_brienne_df.sort_values(by = ['yy-dd-mm','Total Interactions'], ascending=[ filters[filter_date][1], filters[filter_Interactions][1]])




kath_brienne_df = kath_brienne_df.reset_index(drop=True)
kath_brienne_df_copy = kath_brienne_df.copy()
#num_posts = kath_brienne_df_copy.shape[0]
#st.write(f'Total number of posts found: ', str(num_posts))




#print(kath_brienne_df)

#

makes = ['Journalismus','Kommunikation','Digital Kommunikation','Execitive Kommunikation','Kommunikative Wins','Kommunikative Fail','Storymachine','Storymachine Erfolge','Storymachine Lernprozesse','Erfahrungen im journalismus und in der Branche','Gesellschaft','Gewerbeimmobilien','Debatte','Meinung schwerpunktmassig','Philipp Jessen']
make_choice = st.sidebar.selectbox('Select your keyword:', makes)

kath_brienne_df_copy= kath_brienne_df.loc[kath_brienne_df['keyword'] == make_choice]
num_posts = kath_brienne_df_copy.shape[0]
st.write(f'Total number of posts found: ', str(num_posts))

if  num_posts>0:

    kath_brienne_df_copy.reset_index(drop=True, inplace=True)	
    splits = kath_brienne_df_copy.groupby(kath_brienne_df_copy.index // 3)
    for _, frames in splits:
        frames = frames.reset_index(drop=True)
        thumbnails = st.columns(frames.shape[0])
        for i, c in frames.iterrows():
            with thumbnails[i]:
                printFunction(i, c, frames)               
else:
    printError()
