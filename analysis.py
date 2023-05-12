import streamlit as st
from pymongo import MongoClient
import json
import pandas as pd
from pprint import pprint


st.set_page_config(
    layout='wide',
    page_title='Chat Analysis',
    page_icon='🔬'
)


def session_setup():

    if 'data' in st.session_state:
        return

    db_endpoint = st.secrets["db_endpoint"]
    database_info = json.load(open('database.json'))
    db = MongoClient(db_endpoint)[database_info['database']]

    collections = database_info['available_collections']

    data = {}
    for collection in collections:
        documents = db[collection].find({})
        data[collection] = [document for document in documents]

    st.session_state['collections'] = collections
    st.session_state['data'] = data


def annotate(prompt):
    lines = prompt.split('\n')
    res = ''
    human = 1
    ai = 1
    for line in lines:
        if line.startswith('Human:'):
            res = res + 'Human[{}]:'.format(human) + line[6:]
            human += 1
        elif line.startswith('AI:'):
            res = res + 'AI[{}]:'.format(ai) + line[3:]
            ai += 1
        else:
            res = res + line
        res = res + '\n'
    return res


def contains_keywords(prompt):
    prompt = prompt.lower()
    contains = False
    contains |= ('climate' in prompt)
    contains |= ('blm' in prompt)
    contains |= ('black' in prompt)
    return contains


def get_data(collection, annotated, keyword_filters, minimum_response_count):

    # extract data
    data = []
    if collection == 'all':
        for c in st.session_state['data']:
            data = data + st.session_state['data'][c]
    else:
        data = st.session_state['data'][collection]

    # annotate
    if annotated:
        for doc in data:
            doc['prompt'] = annotate(doc['prompt'])

    # filter keywords
    if keyword_filters:
        filtered = []
        for doc in data:
            if contains_keywords(doc['prompt']):
                filtered.append(doc)
        data = filtered

    # minimum response count
    filtered = []
    for doc in data:
        if doc['response_count'] >= minimum_response_count:
            filtered.append(doc)
    data = filtered

    return data


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def main():

    # session setup
    session_setup()

    # select collection
    collection = st.selectbox(
        label='Select collection:',
        options=st.session_state['collections'] + ['all'])

    # select modify options
    st.write('Options')
    annotated = st.checkbox('Annotate conversation index')
    keyword_filters = st.checkbox(
        'Filter out the conversations not mentioning "climate", "blm" or "black"'
    )
    minimum_response_count = st.number_input(
        label='Minimum response count',
        min_value=0,
        max_value=20
    )

    # compute data
    data = get_data(
        collection,
        annotated,
        keyword_filters,
        minimum_response_count
    )

    print(data)

    csv = convert_df(pd.DataFrame(data))
    st.download_button(
        label='Download data',
        data=csv,
        file_name='survey-data-{}.csv'.format(collection),
        mime='text/csv'
    )


if __name__ == '__main__':
    main()
