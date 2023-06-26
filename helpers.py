import pandas as pd
import streamlit as st
from datetime import datetime
import re





month = datetime.today().month
day = datetime.today().day



storymch_logo = "https://storymachine.mocoapp.com/objects/accounts/a201d12e-6005-447a-b7d4-a647e88e2a4a/logo/b562c681943219ea.png"


filters = { 'Total Interaction: High to Low' : ['Total Interactions', False],
            'Total Interaction: Low to High' : ['Total Interactions', True],
            'Posts: Newest First': ['date',False],
            'Posts: Oldest First': ['date',True]}


mapper = { 'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&heroEntityKey=urn%3Ali%3Aorganization%3A12777354&keywords=journalismus&origin=FACETED_SEARCH&position=0&searchId=30c28723-116e-4b63-9a84-82f23f01ce5a&sid=BHt&sortBy=%22date_posted%22' : 'Journalismus' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=kommunikation&origin=GLOBAL_SEARCH_HEADER&sid=VFn&sortBy=%22date_posted%22' : 'Kommunikation' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=digital%20kommunikation&origin=GLOBAL_SEARCH_HEADER&sid=3BI&sortBy=%22date_posted%22' : 'Digital Kommunikation' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=executive%20kommunikation&origin=GLOBAL_SEARCH_HEADER&sid=zjM&sortBy=%22date_posted%22' : 'Execitive Kommunikation' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=kommunikative%20wins&origin=GLOBAL_SEARCH_HEADER&sid=HfO&sortBy=%22date_posted%22' : 'Kommunikative Wins' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=kommunikative%20fails&origin=GLOBAL_SEARCH_HEADER&sid=WTn&sortBy=%22date_posted%22' : 'Kommunikative Fails' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=storymachine&origin=GLOBAL_SEARCH_HEADER&sid=O49&sortBy=%22date_posted%22' : 'Storymachine' ,
            'https://www.linkedin.com/search/results/content/?keywords=storymachine%20erfolge&origin=FACETED_SEARCH&sid=Rl_&sortBy=%22date_posted%22' : 'Storymachine Erfolge' ,
            'https://www.linkedin.com/search/results/content/?keywords=storymachine%20lernprozesse&origin=GLOBAL_SEARCH_HEADER&sid=1y%3B&sortBy=%22date_posted%22' : 'Storymachine Lernprozesse' ,
            'https://www.linkedin.com/search/results/content/?keywords=erfahrungen%20im%20journalismus%20und%20in%20der%20Branche&origin=FACETED_SEARCH&sid=ZI%40&sortBy=%22date_posted%22' : 'Erfahrungen im journalismus und in der Branche' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=gesellschaft&origin=FACETED_SEARCH&sid=qPQ&sortBy=%22date_posted%22' : 'Gesellschaft' ,
            'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=debatte&origin=GLOBAL_SEARCH_HEADER&sid=yw-&sortBy=%22date_posted%22' : 'Debatte' ,
            'https://www.linkedin.com/search/results/content/?keywords=Meinung%20schwerpunktmassig&origin=FACETED_SEARCH&sid=MQ9&sortBy=%22date_posted%22' : 'Meinung schwerpunktmassig' ,
            'https://www.linkedin.com/search/results/content/?keywords=%22Philipp%20Jessen%22&origin=GLOBAL_SEARCH_HEADER&sid=9GJ&sortBy=%22date_posted%22' : 'Philipp Jessen' 


            }


discarded_profiles = []

def read_file(filename):
    df =pd.read_csv(filename)
    df = df.dropna(how='any', subset=['textContent'])
    df.drop(['connectionDegree', 'timestamp'], axis=1, inplace=True)

    df = df[~df['profileUrl'].isin(discarded_profiles)]
    df['postDate'] = df.postUrl.apply(getActualDate)
    df = df.dropna(how='any', subset=['postDate'])
    df['date'] =  pd.to_datetime(df['postDate'])
    df.drop_duplicates(subset=['postUrl'], inplace=True)
    df = df.reset_index(drop=True)
    df['Total Interactions'] = df['likeCount'] + df['commentCount']
    df['likeCount'] = df['likeCount'].fillna(0)
    df['commentCount'] = df['commentCount'].fillna(0)
    df['Total Interactions'] = df['Total Interactions'].fillna(0)
    df['likeCount'] = df['likeCount'].astype(int)
    df['commentCount'] = df['commentCount'].astype(int)
    df['Total Interactions'] = df['Total Interactions'].astype(int)
    df['Keyword']  = df['category']
    df['yy-dd-mm'] = pd.to_datetime(df.date).dt.strftime('%Y/%m/%d')

    df['keyword'] =  df['query'].apply(lambda x : mapper[x])

    
    return df




def read_file_sp(filename):
    df =pd.read_csv(filename)
    df = df.dropna(how='any', subset=['postContent'])
    # df.drop(['error', 'timestamp', 'sharedPostUrl','sharedPostProfileUrl',
    #         'sharedJobUrl','videoUrl','sharedPostCompanyUrl'], axis=1, inplace=True)

    df['postDate'] = df.postUrl.apply(getActualDate)
    df = df.dropna(how='any', subset=['postDate'])
    df['date'] =  pd.to_datetime(df['postDate'])

    df['company_name'] =  df.profileUrl.apply(lambda x : mapper[x])
    

    df.drop_duplicates(subset=['postUrl'], inplace=True)
    df = df.reset_index(drop=True)
    df['Total Interactions'] = df['likeCount'] + df['commentCount']
    df['likeCount'] = df['likeCount'].fillna(0)
    df['commentCount'] = df['commentCount'].fillna(0)
    df['Total Interactions'] = df['Total Interactions'].fillna(0)
    df['likeCount'] = df['likeCount'].astype(int)
    df['commentCount'] = df['commentCount'].astype(int)
    df['Total Interactions'] = df['Total Interactions'].astype(int)
    #df['Keyword']  = df['category']
    df['yy-dd-mm'] = pd.to_datetime(df.date).dt.strftime('%Y/%m/%d')
    
    return df






def getActualDate(url):
    a= re.findall(r"\d{19}", url)
    a = int(''.join(a))
    a = format(a, 'b')
    first41chars = a[:41]
    ts = int(first41chars,2)
    actualtime = datetime.fromtimestamp(ts/1000).strftime("%Y-%m-%d %H:%M:%S %Z")
    return actualtime



def printFunction(i, rows, dataframe):
   
    if not pd.isnull(rows['companyUrl']):
        st.subheader(rows.companyName)
        st.write('Company Account')
      
        st.info(rows['textContent'])
        st.write('Total Interactions 📈:  ',rows['Total Interactions'])
        st.write('Likes 👍:  ',rows['likeCount']) 
        st.write('Comments 💬:  ',rows['commentCount'])
        st.write('Publish Date & Time 📆:         ',rows['postDate']) #publishDate
        with st.expander('Link to this Post 📮'):
                st.write(rows['postUrl']) #linktoPost
        with st.expander('Link to  Profile 🔗'):
                st.write(rows['companyUrl']) #linktoProfile


    if not pd.isnull(rows['profileUrl']):
        #st.image(rows['profileImgUrl'], width=150)
        st.subheader(dataframe.fullName[i])
        st.write('Personal Account')
        st.write(rows['title']) #postType
        st.write('-----------')
       
        st.info(rows['textContent'])  #postrowsontent
        st.write('Total Interactions 📈:  ',rows['Total Interactions']) #totInterarowstions
        st.write('Likes 👍:  ',rows['likeCount']) #totInterarowstions
        st.write('Comments 💬:  ',rows['commentCount']) #totInterarowstions
        #st.write('Arowstion 📌:  ',rows['arowstion']) #totInterarowstions
        st.write('Publish Date & Time 📆:         ',rows['postDate']) #publishDate
        with st.expander('Link to this Post 📮'):
                st.write(rows['postUrl']) #linktoPost
        with st.expander('Link to  Profile 🔗'):
                st.write(rows['profileUrl']) #linktoProfile




def printFunction_search(i, rows, dataframe):
   
    if not pd.isnull(rows['profileUrl']):
        #st.image(rows['profileImgUrl'], width=150)
        st.subheader(dataframe.fullName[i])
        st.write('Personal Account')
        st.write(rows['title']) #postType
        st.write('-----------')
       
        st.info(rows['textContent'])  #postrowsontent
        st.write('Total Interactions 📈:  ',rows['Total Interactions']) #totInterarowstions
        st.write('Likes 👍:  ',rows['likeCount']) #totInterarowstions
        st.write('Comments 💬:  ',rows['commentCount']) #totInterarowstions
        #st.write('Arowstion 📌:  ',rows['arowstion']) #totInterarowstions
        st.write('Publish Date & Time 📆:         ',rows['postDate']) #publishDate
        with st.expander('Link to this Post 📮'):
                st.write(rows['postUrl']) #linktoPost
        with st.expander('Link to  Profile 🔗'):
                st.write(rows['profileUrl']) #linktoProfile
    



def printFunction_posts(i, rows, dataframe):
    if not pd.isnull(rows['profileUrl']):
        
        st.subheader(dataframe.company_name[i])
        st.write('Content Type: ', rows['type']) #postType
        st.write('-----------')
        if 'imgUrl' in dataframe.columns:
            # if rows['imgUrl']:
            #     st.image(rows['imgUrl'], width=230)

            if not pd.isnull(rows['imgUrl']):
                        st.image(rows['imgUrl'])

        st.info(rows['postContent'])  #postrowsontent
        st.write('Total Interactions 📈:  ',rows['Total Interactions']) #totInterarowstions
        st.write('Likes 👍:  ',rows['likeCount']) #totInterarowstions
        st.write('Comments 💬:  ',rows['commentCount']) #totInterarowstions
        #st.write('Arowstion 📌:  ',rows['arowstion']) #totInterarowstions
        st.write('Publish Date & Time 📆:         ',rows['postDate']) #publishDate
        with st.expander('Link to this Post 📮'):
                st.write(rows['postUrl']) #linktoPost
        with st.expander('Link to  Profile 🔗'):
                st.write(rows['profileUrl']) #linktoProfile
    





def printError():
    st.image('https://img.freepik.com/premium-vector/hazard-warning-attention-sign-with-exclamation-mark-symbol-white_231786-5218.jpg?w=2000', width =200)
    st.subheader('Oops... No new post found in last Hours.')


def printAccountInfo(dataframe, option):
    dataframe_copy = dataframe[dataframe.Branche == option]
    dataframe_copy = dataframe_copy.reset_index(drop=True)
    num_post = dataframe_copy.shape[0]
    if num_post>0:
        splits = dataframe_copy.groupby(dataframe_copy.index//3)
        for _,frame in splits:
            frame = frame.reset_index(drop=True)
            thumbnail = st.columns(frame.shape[0])
            for i, row in frame.iterrows():
                with thumbnail[i]:
                    st.subheader(row['Account_Name'])
                    if not pd.isnull(row['imgUrl']):
                        st.image(row['imgUrl'])
                    st.info(row['postContent'])
                    st.write('Publish Date & Time 📆:         ',row['postDate'])
                    st.write('Total Interactions 📈:  ',row['Total Interactions'])
                    st.write('Likes 👍:  ',row['likeCount']) #totInteractions
                    st.write('Comments 💬:  ',row['commentCount']) #totInteractions
                    with st.expander('Link to this Post 📮'):
                        st.write(row['postUrl']) #linktoPost
                    with st.expander('Link to  Profile 🔗'):
                        st.write(row['profileUrl']) #linktoProfile
    else:
        st.image('https://img.freepik.com/premium-vector/hazard-warning-attention-sign-with-exclamation-mark-symbol-white_231786-5218.jpg?w=2000', width =200)
        st.subheader('Oops... No new post found for the selection.')

