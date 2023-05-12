import streamlit as st


minimum_responses = 6
warning_responses = 10
maximum_responses = 12


# Show response count
def show_response_count():

    response_count = st.session_state['response_count']

    if response_count == 0:
        return

    response_count_message = "You have finished {} round(s) of conversation.".format(
        response_count)

    # Need more responses
    if response_count < warning_responses:
        st.info(response_count_message)

    # Enough but can ask more
    if warning_responses <= response_count < maximum_responses:
        extra_count = maximum_responses - response_count
        response_count_message += ' Due to time limit, you can only ask {} more question to the chatbot.'.format(
            extra_count)
        st.warning(response_count_message)

    # Done
    if maximum_responses <= response_count:
        st.success(response_count_message)


# Push button to finish the survey
def finish_button():

    response_count = st.session_state['response_count']

    if response_count == maximum_responses:
        st.session_state['survey_finished'] = True

    if not st.session_state['survey_finished'] and response_count >= minimum_responses:
        st.session_state['survey_finished'] |= st.button('Finish Chat')


# Show the survey completed message
def show_finish_status():

    if not st.session_state['survey_finished']:
        return

    survey_id = st.session_state['survey_id']
    st.success(f'''
      **Chat completed!** Thank you for chatting with GPT-3! \n
      Please return to the survey page and paste this verification code: **{survey_id}**. 
      You can now close this page if you have submitted this code in survey.
    ''')
