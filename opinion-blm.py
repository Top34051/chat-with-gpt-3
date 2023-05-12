import streamlit as st

from utils.session import session_setup, modify_prompt, modify_chat_history
from utils.components import show_response_count, finish_button, show_finish_status
from utils.chatbot import get_response
from utils.database import submit_to_database


st.set_page_config(
    layout='wide',
    page_title='GPT-3 chatbot',
    page_icon='🤖'
)


def main():

    # Set up session
    session_setup()

    # Show information
    st.title('GPT-3 chatbot')
    st.info(
        'Your goal is to **exchange your opinion** with GPT-3 on **black lives matter**.'
    )

    # Show chat history
    st.text_area(
        'Chat history',
        value=st.session_state['chat_history'],
        height=500
    )

    # Get the user input
    user_input = st.text_input(
        'You:',
        value='',
        key=str(st.session_state['response_count'])
    )

    # Get the response from gpt-3 (None if not possible)
    response = get_response(user_input)

    # Save response
    if response != None:

        # Modify prompt
        modify_prompt(user_input, response)

        # Modify chat history
        modify_chat_history(user_input, response)

        # Increment response count
        st.session_state['response_count'] += 1

        # Rerun page
        st.experimental_rerun()

    # Show response count
    show_response_count()

    # Update session status
    finish_button()

    # Show finish status
    show_finish_status()

    # Submit survey to database if finished
    submit_to_database('opinion-blm')


if __name__ == '__main__':
    main()
