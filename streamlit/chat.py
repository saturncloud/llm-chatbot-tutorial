import streamlit as st
import os

from llm_chatbot_tutorial.fsstreamlit import StreamlitChatLoop

st.set_page_config(page_title="chat", page_icon=":robot_face:", layout='wide')


@st.cache_resource
def load_models():
    chat = StreamlitChatLoop(os.getenv('MODEL_PATH', "lmsys/vicuna-7b-v1.3"))
    chat.load_models()
    return chat

chat = load_models()

output = st.text('')

def clear_conversation():
    chat.clear_conversation()

st.button('Clear Conversation', on_click=clear_conversation)


with st.form(key='input-form', clear_on_submit=True):
    user_input = st.text_area("You:", key='input', height=100)
    submit_button = st.form_submit_button(label='Send')


if not submit_button:
    st.stop()

chat.take_user_input(user_input)
messages = [f'{role}: {"" if message is None else message}' for role, message in chat.conv.messages]
message_string = "\n\n".join(messages)
for text in chat.loop():
    message = message_string + text
    message = message.replace('\n', '\n\n')
    output.write(message)
