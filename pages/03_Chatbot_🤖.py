import streamlit as st
import openai
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env
load_dotenv()

# Access the OpenAI API key from the secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize client for new Assistants API usage
client = openai.Client()  # This requires openai >= 0.28.0

# Track conversation in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    # Create a new thread for the conversation
    new_thread = client.beta.threads.create()
    st.session_state.thread_id = new_thread.id

# Streamlit page config
st.set_page_config(
    page_title="Oil AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("Oil AI Assistant 🤖")
st.markdown("Chat with our AI assistant about oil and gas industry topics or with your custom datasets.")
st.divider()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me anything about your datasets or gas industry..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to the Thread in the Assistants API
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=prompt
    )

    # Trigger the Assistant run using the existing assistant_id
    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id="asst_1lRqEQtymcXvb2rbmrErSQGY",
    )

    # Optionally wait for run to complete (polling approach)
    while True:
        current_run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread_id,
            run_id=run.id
        )
        if current_run.status == "completed":
            break
        if current_run.status == "failed":
            st.error("Assistant run failed.")
            break
        time.sleep(2)

    # Retrieve updated messages, parse latest assistant response
    updated_messages = client.beta.threads.messages.list(
        thread_id=st.session_state.thread_id,
        order="asc"
    ).data

    # Last message should be from the assistant
    assistant_message = None
    for msg_obj in reversed(updated_messages):
        if msg_obj.role == "assistant":
            for content_part in msg_obj.content:
                if content_part.type == "text":
                    assistant_message = content_part.text.value
            break

    if assistant_message is None:
        assistant_message = "I'm sorry, I couldn't retrieve a response at this time."

    # Display the assistant's message
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

# Sidebar
with st.sidebar:
    # st.markdown("### Chat Information")
    # st.markdown(f"Messages in conversation: {len(st.session_state.messages)}")
    st.markdown(
        """
        ### Example Questions
        - List all your datasets and summarize them for me
        - List all the columns in your datasets
        - Make me some visualizations and general statistics of the first dataset
        - Make me a report of the first dataset
        """
    )
    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
