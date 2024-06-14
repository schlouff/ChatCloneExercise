import streamlit as st
import os
import time
import openai

from openai import OpenAI

st.write("DB username:", st.secrets["Christo"])
st.write("DB password:", st.secrets["ba11one"])
st.write("My cool secrets:", st.secrets["my_cool_secrets"]["things_i_like"])

# And the root-level secrets are also accessible as environment variables:
st.write(
    "Has environment variables been set:",
    os.environ["db_username"] == st.secrets["db_username"],
)

openai.api_key = api_key

openai.api_key = api_key


openai.api_key = api_key

client = OpenAI()

# Initialisierungen
questions = list()
bot_responses = list()
messages = list()

system_prompt = 'Answer as concisely as possible.'
messages.append({'role': 'system', 'content': system_prompt})

def chat_with_bot(user_input):
    messages.append({'role': 'user', 'content': user_input})
    questions.append(user_input)

    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.7,
    )

    current_response = completion.choices[0].message.content
    bot_responses.append(current_response)
    messages.append({'role': 'assistant', 'content': current_response})
    return current_response

if __name__ == '__main__':
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.title('Chat Bot')
    with col2:
        st.image('ai.png', width=70)

    with st.form(key='chat_form'):
        user_input = st.text_input('You:', '')

        submit_button = st.form_submit_button(label='Send')

        if submit_button:
            if user_input.lower() in ['exit', 'quit']:
                st.write('Chat Bot: I was happy to assist you. Bye bye!')
                time.sleep(2)
                st.stop()

            if user_input.lower() == '':
                st.warning('Please enter a message.')
            else:
                response = chat_with_bot(user_input)
                st.write(f'Chat Bot: {response}')

                if 'history' not in st.session_state:
                    st.session_state['history'] = f'You: {user_input}\nChat Bot: {response}\n'
                else:
                    st.session_state['history'] += f'You: {user_input}\nChat Bot: {response}\n'

                st.text_area(label='Chat History', value=st.session_state['history'], height=400)
