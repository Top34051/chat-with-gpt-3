import streamlit as st
import openai
import os


st.set_page_config(layout='wide', page_title='GPT-3 chatbot')
openai.api_key = OPENAI_API_KEY


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
  
  user_input = get_text()
  if user_input != '':

    # add user input to prompt
    st.session_state['prompt'] = st.session_state['prompt'] + 'Human: ' + user_input + '\n' + 'AI:'
    
    # get response from bot
    response = get_response().choices[0].text
    st.text_area("Bot:", value=response, height=200, max_chars=None, key=None)
    
    # add response to prompt
    st.session_state['prompt'] = st.session_state['prompt'] + response + '\n'
    st.session_state['response_count'] += 1

    st.write('Response count:', st.session_state['response_count'])

  # submit survey
  with st.form(key='submit_form'):
    survey_id = st.text_input('Your survey identification number')
    clicked = st.form_submit_button('Complete survey')
    if clicked:
      if st.session_state['response_count'] >= 20:
        st.success('Survey completed! Please close this window and complete a post-survey.')
        # save prompt
      else:
        st.error('Please make more conversation with the chatbot') 


if __name__ == '__main__':
  main()