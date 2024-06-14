import streamlit as st
import openai
import os

# Versuche, die API-Schlüssel aus den Streamlit Secrets zu laden
try:
    api_key = st.secrets["api"]["api_key"]
    assert api_key.startswith('sk-'), 'Error loading the API key. The API key starts with "sk-"'
    os.environ['OPENAI_API_KEY'] = api_key

    openai.api_key = api_key

    st.write("API key successfully loaded.")
except KeyError as e:
    st.error(f"KeyError: {str(e)} - Please check if the secret 'api_key' is correctly configured.")
except AssertionError as e:
    st.error(f"AssertionError: {str(e)}")
except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")

# Initialisierungen
questions = []
bot_responses = []
messages = []

system_prompt = 'Answer as concisely as possible.'
messages.append({'role': 'system', 'content': system_prompt})

def chat_with_bot(user_input):
    messages.append({'role': 'user', 'content': user_input})
    questions.append(user_input)

    try:
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.7,
        )

        current_response = completion.choices[0].message['content']
        bot_responses.append(current_response)
        messages.append({'role': 'assistant', 'content': current_response})
        return current_response
    except Exception as e:
        st.error(f"Error communicating with OpenAI: {str(e)}")
        return "Error"

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
