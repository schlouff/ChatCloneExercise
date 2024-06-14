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
    "Hallo. Schön, dass du hier bist.\n\nDu hast jetzt die Möglichkeit eine Situation zu untersuchen, die bei dir Scham ausgelöst hat, die dir peinlich/unangenehm war und es vielleicht noch ist. Was für eine peinliche oder schamauslösende Situation fällt dir ein? Du wirst mit der Erinnerung an diese Situation weiterarbeiten. Wenn du merkst, das ist jetzt gerade zu krass, vielleicht gibt es ja auch eine Situation, in der du nicht so tief einsteigst, aber wo das Gefühl auch wieder auftaucht.\nDu übernimmst die Verantwortung für dich selbst in dieser Arbeit, aber wir geben dir Raum und Zeit zum reflektieren und vielleicht sogar anstöße das Gefühl zu der Situation zu verändern. Also bist du startklar?\nSchreib “ok” - und dann kann es losgehen.",
    "Schau, welche Peinliche/schamhafte Situation heute für dich passt. Schau mal in deinem inneren, was du alles siehst in dieser Situation und was du dabei fühlst. Lass dir dabei zeit und schreib “ok” wenn du eine Situation vor Augen hast.",
    "Gibt es in dieser Situation etwas, dass jemand gesagt hat? Was ein bestimmtes Gefühl ausgelöst hat? Gibt es was was dir an dieser Situation besonders auffällt vielleicht ein Detail?\nSchreib “ok”, wenn es weitergehen kann.",
    "Jetzt überleg mal. Kannst du dieser Situation einen Namen geben? Oder eine Überschrift? Die Überschrift kann sich darauf beziehen, oder ein Headliner sein.\nWas wäre ein Songtitel für diese Situation? Schreibe die Überschrift oder den Songtitel in das unten liegende Feld. Bitte verzichte hier auf konkrete Namen(eigentlich hatten wir diese Aufgabe im Kopf gemacht weil da auch krasse sachen rauskommen können die vielleicht so nicht ausgesprochen werden müssen. )\nJetzt schreib den Namen auf.",
    "Wenn diese Situation ein Bild bekommen würde, wie sähe das aus?\nWas für eine Landschaft wäre diese Situation? Eine Landschaft kann irgendein Ort sein, kann auch in der Stadt sein oder ein Raum. Das muss gar nichts mit dem Ort zu tun haben, wo die Situation stattgefunden hat. Es geht eher um das Gefühl von der Situation. Ist das eng, oder ganz weit?\nBeschreib jetzt diese Landschaft. Wie sieht sie aus?\n",
    "Vielleicht ist es eher ein Tier? Vielleicht denkt ihr an euch, was für ein Tier ihr gewesen wärt, z.b. wie eine Maus, die sich verkrümeln wollte oder ihr denkt an das Gegenüber welches Tier wäre das im Vergleich zu euch gewesen. Beschreibt dieses Tier wie sieht das aus.\nNimm dir Zeit, wenn du deine Landschaft oder dein Tier vor Augen hast schreib alles dazu unten in das Feld hinein.",
    "Super, du hast jetzt ein Gefühl, eine Überschrift und ein Bild. Du hast gerade gesehen, wie Kunst entstehen kann.\n\nJetzt soll die Bildbeschreibung kreiert werden."
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
        f"Erstelle (auf deutsch) eine künstlerische Beschreibung, die auf den Eingaben beruht:\n"
        f"1. Situation: {responses[0]}\n"
        f"2. Situation Details: {responses[1]}\n"
        f"3. Detail: {responses[2]}\n"
        f"4. Title: {responses[3]}\n"
        f"5. Landscape: {responses[4]}\n"
        f"6. Animal (if applicable): {responses[5] if len(responses) > 5 else 'N/A'}"
    )

    messages.append({'role': 'user', 'content': description_prompt})
    
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.7,
    )

    artistic_description = completion.choices[0].message.content
    return artistic_description

def generate_image(prompt):
    dalle_prompt = {
        "prompt": f"{prompt}, in the style of Egon Schiele",
        "size": "1024x1024"
    }
    response = client.images.generate(**dalle_prompt)
    return response['data'][0]['url']

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
                st.session_state.responses.append(user_input)

                if 'history' not in st.session_state:
                    st.session_state['history'] = f'You: {user_input}\n'
                else:
                    st.session_state['history'] += f'You: {user_input}\n'

                st.text_area(label='Chat History', value=st.session_state['history'], height=400)

                if st.session_state.current_question_index < len(questions) - 1:
                    st.session_state.current_question_index += 1
                elif st.session_state.current_question_index == len(questions) - 1:
                    artistic_description = create_artistic_description(st.session_state.responses)
                    image_url = generate_image(artistic_description)
                    st.image(image_url, caption='Generated Image', use_column_width=True)
                    st.session_state.current_question_index += 1
