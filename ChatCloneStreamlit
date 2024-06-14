import streamlit as st
import os
import time
import openai

from openai import OpenAI

api_key = st.secrets["api"]["api_key"]
assert api_key.startswith('sk-'), 'Error loading the API key. The API key starts with "sk-"'
os.environ['OPENAI_API_KEY'] = api_key

openai.api_key = api_key

client = OpenAI()

# Initialisierungen
questions = [
    "Think of a situation.",
    "What animal does this situation remind you of?",
    "In what landscape is this animal?",
    "Add an item that gives you strength or a good feeling."
]
bot_responses = list()
messages = list()

system_prompt = 'Answer as concisely as possible.'
messages.append({'role': 'system', 'content': system_prompt})

def chat_with_bot(user_input):
    messages.append({'role': 'user', 'content': user_input})

    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.7,
    )

    current_response = completion.choices[0].message.content
    bot_responses.append(current_response)
    messages.append({'role': 'assistant', 'content': current_response})
    return current_response

def create_artistic_description(responses):
    description_prompt = (
        f"Create an artistic image description based on the following inputs:\n"
        f"1. Situation: {responses[0]}\n"
        f"2. Animal: {responses[1]}\n"
        f"3. Landscape: {responses[2]}\n"
        f"4. Item: {responses[3]}"
    )

    messages.append({'role': 'user', 'content': description_prompt})
    
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.7,
    )

    artistic_description = completion.choices[0].message.content
    return artistic_description

if __name__ == '__main__':
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.title('Chat Bot')
    with col2:
        st.image('ai.png', width=70)

    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0

    if 'responses' not in st.session_state:
        st.session_state.responses = []

    with st.form(key='chat_form'):
        if st.session_state.current_question_index < len(questions):
            current_question = questions[st.session_state.current_question_index]
        else:
            current_question = "Thank you for your responses. How else can I assist you?"

        st.write(f'Chat Bot: {current_question}')
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

                if st.session_state.current_question_index < len(questions):
                    st.session_state.responses.append(user_input)
                    st.session_state.current_question_index += 1
                else:
                    st.session_state.responses.append(user_input)
                    artistic_description = create_artistic_description(st.session_state.responses)
                    st.write(f'Artistic Description: {artistic_description}')

