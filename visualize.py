import streamlit as st
from pymongo import MongoClient
import json
import pandas as pd

st.set_page_config(layout='wide', page_title='GPT-3 chatbot')

mongodb_uri = st.secrets["MONGODB_URI"]


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def init():

    if 'document' not in st.session_state:
        cluster = MongoClient(mongodb_uri)
        database = json.load(open('database.json'))
        db = cluster[database['database']]
        collection = db[database['collection']]
        documents = collection.find({})
        st.session_state['document'] = [document for document in documents]

    if 'document_csv' not in st.session_state:
        st.session_state['document_csv'] = pd.DataFrame(
            st.session_state['document'])


if __name__ == '__main__':

    init()

    csv = convert_df(st.session_state['document_csv'])
    st.sidebar.download_button(
        label='Download all data',
        data=csv,
        file_name='pilot-survey.csv',
        mime='text/csv'
    )

    st.title('Visualize data')

    idx = int(st.number_input('Document number',
                              1, len(st.session_state['document'])))

    document = st.session_state['document'][idx-1]
    st.write(f"**Verification code**: {document['_id']}")
    st.write(f"**Response count**: {document['response_count']}")
    st.write(f"**Timestamp**: {document['timestamp']}")
    st.text_area('Prompt', document['prompt'], height=1000)
