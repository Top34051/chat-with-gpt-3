import streamlit as st
import pymongo
from pymongo import MongoClient
import json
import datetime


db_endpoint = st.secrets["db_endpoint"]


def submit_to_database(survey_type):

    # Survey is not finished yet
    if not st.session_state['survey_finished']:
        return

    survey_id = st.session_state['survey_id']
    response_count = st.session_state['response_count']
    prompt = st.session_state['prompt']
    timestamp = datetime.datetime.now()

    data = {
        '_id': survey_id,
        'response_count': response_count,
        'prompt': prompt,
        'survey_type': survey_type,
        'timestamp': timestamp
    }

    database = json.load(open('database.json'))
    cluster = MongoClient(db_endpoint)
    db = cluster[database['database']]
    collection = db[database['collection']]

    # New entry to the database
    if not st.session_state['submitted_to_database']:
        collection.insert_one(data)

    # Modify entry in the database
    else:
        collection.find_and_modify(
            query={'_id': survey_id},
            update={
                '$set': data
            },
            upsert=False
        )

    st.session_state['submitted_to_database'] = True
