import streamlit as st
from streamlit_chat import message
from audio_recorder_streamlit import audio_recorder
import time
from language_bot import LanguageBot


st.title('Language GPT Buddy')
st.subheader("Language GPT Buddy is an app utilizing OpenAI's API for interactive language learning with a conversational AI. It offers both text and voice interactions in multiple languages, tailoring to the user's proficiency.")

st.text_input("Openai api key", key="key")


col1, col2 = st.columns(2)

with col1:
    level = st.radio(
        "Set your language level",
        key="language_level",
        options=["Beginner", "Intermediate", "Advanced"],
    )

with col2:
    language = st.selectbox(
        'Choose language',
        ('Spanish', 'Italian', 'German')
    )


st.title("Language GPT Buddy")

language_bot = LanguageBot()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": language_bot.get_prompt(language, level)})


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] != "system":
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter chat message"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


# Display assistant response in chat message container
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    assistant_response = language_bot.get_answer(st.session_state.messages)

    # Simulate stream of response with milliseconds delay
    for chunk in assistant_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "")
    message_placeholder.markdown(full_response)

# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": full_response})


# st.title("Audio Recorder")
# audio_bytes = audio_recorder()
# if audio_bytes:
#    st.audio(audio_bytes, format="audio/wav")
