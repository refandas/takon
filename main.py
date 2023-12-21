import google.generativeai as genai
import streamlit as st

st.title("Takon")

# Initialize Google API
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = "gemini-pro"

model = genai.GenerativeModel(st.session_state["gemini_model"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    # Display use message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        messages = [
            {
                "role": message["role"],
                "parts": message["content"]
            }
            for message in st.session_state.messages
        ]

        with st.spinner("Wait for it..."):
            response = model.generate_content(messages)
            message_placeholder.markdown(response.text)

    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "model",
        "content": response.text,
    })
