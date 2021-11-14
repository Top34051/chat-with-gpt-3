import streamlit as st
import openai
import os
import random


st.set_page_config(layout='wide', page_title='GPT-3 chatbot')
openai.api_key = st.secrets["OPENAI_API_KEY"]

response_limit = [3, 5]


def get_text():
  input_text = st.text_input("You: ")
  return input_text


def get_response():
  start_sequence = "\nAI:"
  restart_sequence = "\nHuman: "

  print('prompt:', st.session_state['prompt'])

  response = openai.Completion.create(
    engine="davinci",
    prompt=st.session_state['prompt'],
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=["\n", " Human:", " AI:"]
  )

  print('response:', response)
  return response


def main():
  st.title('GPT-3 chatbot')

  if 'prompt' not in st.session_state:
    st.session_state['prompt'] = 'The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\n'
  if 'response_count' not in st.session_state:
    st.session_state['response_count'] = 0
  if 'survey_id' not in st.session_state:
    st.session_state['survey_id'] = random.randint(100000, 999999)
  
  user_input = get_text()
  if user_input != '':

    # add user input to prompt
    st.session_state['prompt'] = st.session_state['prompt'] + 'Human: ' + user_input + '\n' + 'AI:'
    
    if st.session_state['response_count'] < response_limit[1]:

      # get response from bot
      response = get_response().choices[0].text
      st.text_area("Bot:", value=response, height=200, max_chars=None, key=None)
      
      # add response to prompt
      st.session_state['prompt'] = st.session_state['prompt'] + response + '\n'
      st.session_state['response_count'] += 1

    response_count_message = f"Response count: {st.session_state['response_count']}"
    if st.session_state['response_count'] < response_limit[0]:
      st.success(response_count_message)
    elif st.session_state['response_count'] < response_limit[1]:
      extra_count = response_limit[1] - st.session_state['response_count']
      st.warning(response_count_message + f'. The survey has ended, but you can ask {extra_count} more questions.')
    else:
      st.error(response_count_message + '. The survey has ended!')


  # submit survey
  if st.session_state['response_count'] >= response_limit[0]:
    survey_id = st.session_state['survey_id']
    st.success(f'**Survey completed!**\n\n{survey_id} is your identification number. Please close this window, return to the post-survey and put this number in.')


if __name__ == '__main__':
  main()