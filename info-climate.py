import streamlit as st
import openai
import os
import random
import string
import pymongo
from pymongo import MongoClient
import datetime
import json


st.set_page_config(layout='wide', page_title='GPT-3 chatbot')

openai.api_key = st.secrets["OPENAI_API_KEY"]
mongodb_uri = st.secrets["MONGODB_URI"]

response_limit = [6, 10, 12]

m = st.markdown("""
<style>
div.stButton > button:first-child {
    height: 50px;
}
</style>""", unsafe_allow_html=True)


def get_text():
  input_text = st.text_input("You: ")
  return input_text


def content_filter(content_to_classify):
  response = openai.Completion.create(
    engine="content-filter-alpha",
    prompt = "<|endoftext|>" + content_to_classify + "\n--\nLabel:",
    temperature=0,
    max_tokens=1,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    logprobs=10
  )
  output_label = response["choices"][0]["text"]

  # This is the probability at which we evaluate that a "2" is likely real
  # vs. should be discarded as a false positive
  toxic_threshold = -0.355

  if output_label == "2":
      # If the model returns "2", return its confidence in 2 or other output-labels
      logprobs = response["choices"][0]["logprobs"]["top_logprobs"][0]

      # If the model is not sufficiently confident in "2",
      # choose the most probable of "0" or "1"
      # Guaranteed to have a confidence for 2 since this was the selected token.
      if logprobs["2"] < toxic_threshold:
          logprob_0 = logprobs.get("0", None)
          logprob_1 = logprobs.get("1", None)

          # If both "0" and "1" have probabilities, set the output label
          # to whichever is most probable
          if logprob_0 is not None and logprob_1 is not None:
              if logprob_0 >= logprob_1:
                  output_label = "0"
              else:
                  output_label = "1"
          # If only one of them is found, set output label to that one
          elif logprob_0 is not None:
              output_label = "0"
          elif logprob_1 is not None:
              output_label = "1"

          # If neither "0" or "1" are available, stick with "2"
          # by leaving output_label unchanged.

  # if the most probable token is none of "0", "1", or "2"
  # this should be set as unsafe
  if output_label not in ["0", "1", "2"]:
      output_label = "2"

  return output_label


def get_response():

  print('prompt:', st.session_state['prompt'])

  response = openai.Completion.create(
    engine="davinci",
    prompt=st.session_state['prompt'],
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=["\n", " Human:", " AI:"],
    user=st.session_state['survey_id']
  )

  print('response:', response)

  content = response.choices[0].text
  if content_filter(content) != '2':
    return response
  return get_response()

def get_survey_id():
  # [0-9][0-9][A-Z][A-Z][A-Z][0-9][0-9][A-Z][0-9][A-Z].
  survey_id = ''
  survey_id = survey_id + str(random.randint(0, 9))
  survey_id = survey_id + str(random.randint(0, 9))
  survey_id = survey_id + random.choice(string.ascii_letters)
  survey_id = survey_id + random.choice(string.ascii_letters)
  survey_id = survey_id + random.choice(string.ascii_letters)
  survey_id = survey_id + str(random.randint(0, 9))
  survey_id = survey_id + str(random.randint(0, 9))
  survey_id = survey_id + random.choice(string.ascii_letters)
  survey_id = survey_id + str(random.randint(0, 9))
  survey_id = survey_id + random.choice(string.ascii_letters)
  return survey_id

def main():

  # session states
  if 'prompt' not in st.session_state:
    st.session_state['prompt'] = 'The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\n'
  
  # session states
  if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = 'Your chat with GPT-3 will appear here!\n\n'

  if 'response_count' not in st.session_state:
    st.session_state['response_count'] = 0
  
  if 'survey_id' not in st.session_state:
    st.session_state['survey_id'] = get_survey_id()

  if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

  if 'finished' not in st.session_state:
    st.session_state['finished'] = False

  st.title('GPT-3 chatbot')

  instruction_text = 'Your goal is to **find out the information** with GPT-3 about **climate change**.'
  st.info(instruction_text)

  chat_history = st.empty()
  chat_history.text_area('Chat history', value=st.session_state['chat_history'], height=275)
  
  user_input = get_text()

  if user_input != '':
    
    if st.session_state['response_count'] < response_limit[2] and not st.session_state['finished']:

      # add user input to prompt
      st.session_state['prompt'] = st.session_state['prompt'] + 'Human: ' + user_input + '\n' + 'AI:'

      # get response from bot
      response = get_response().choices[0].text
      
      # add response to prompt
      st.session_state['prompt'] = st.session_state['prompt'] + response + '\n'
      st.session_state['response_count'] += 1

      # update chat history
      st.session_state['chat_history'] = st.session_state['chat_history'] + 'Participant: ' + user_input + '\n'
      st.session_state['chat_history'] = st.session_state['chat_history'] + 'GPT-3: ' + response + '\n'
      chat_history.text_area('Chat history', value=st.session_state['chat_history'], height=275)

    if st.session_state['response_count'] == 1:
      response_count_message = f"You have finished {st.session_state['response_count']} round of conversation."
    else:
      response_count_message = f"You have finished {st.session_state['response_count']} rounds of conversation."

    if st.session_state['response_count'] < response_limit[1]:
      st.info(response_count_message)

    elif st.session_state['response_count'] < response_limit[2]:
      extra_count = response_limit[2] - st.session_state['response_count']
      st.warning(response_count_message + f' Due to time limit, you can only ask {extra_count} more question to the chatbot.')

    else:
      st.success(response_count_message)

    if not st.session_state['finished'] and response_limit[0] <= st.session_state['response_count'] < response_limit[2]:
      st.session_state['finished'] |= st.button('Finish Chat')
      print('st.session_state:', st.session_state['finished'])

    if st.session_state['response_count'] == response_limit[2]:
      st.session_state['finished'] = True


  # submit survey
  if st.session_state['finished']:
    
    survey_id = st.session_state['survey_id']
    st.success(f'''
      **Chat completed!** Thank you for chatting with GPT-3! \n
      Please return to the survey page and paste this verification code: **{survey_id}**. 
      You can now close this page if you have submitted this code in survey.
    ''')

    # update database
    database = json.load(open('database.json'))
    cluster = MongoClient(mongodb_uri)
    db = cluster[database['database']]
    collection = db[database['collection']]

    if not st.session_state['submitted']:
      collection.insert_one({
        '_id': survey_id,
        'response_count': st.session_state['response_count'],
        'prompt': st.session_state['prompt'],
        'timestamp': datetime.datetime.now()
      })
    
    else:
      collection.find_and_modify(
        query = {'_id': survey_id},
        update = {
          '$set': {
            '_id': survey_id,
            'response_count': st.session_state['response_count'],
            'prompt': st.session_state['prompt'],
            'timestamp': datetime.datetime.now()
          }
        },
        upsert=False
      )

    st.session_state['submitted'] = True


if __name__ == '__main__':
  main()