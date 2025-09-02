import streamlit as st
import requests

st.set_page_config(page_title="Customer Support Chatbot", layout="wide")

st.title("💬 Smart Customer Support Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Send to Rasa REST API
    response = requests.post(
        "http://localhost:5005/webhooks/rest/webhook",
        json={"sender": "user", "message": prompt}
    )

    bot_reply = response.json()[0]['text']
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").markdown(bot_reply)