import streamlit as st
import openai
from datetime import datetime

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def main():
    st.set_page_config(
        page_title="Oil AI Chatbot",
        page_icon="🤖",
        layout="wide"
    )

    init_session_state()

    st.title("Oil AI Assistant 🤖")
    st.markdown("Chat with our AI assistant about oil and gas industry topics.")
    st.divider()

    # Chat interface
    chat_container = st.container()
    with chat_container:
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask me anything about oil and gas..."):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Add assistant response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                # For now, just echo back a simple response
                response = f"I understand you're asking about: {prompt}\n\nThis is a placeholder response. API integration will be implemented soon."
                message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    # Sidebar for chat controls
    with st.sidebar:
        st.title("Chat Controls")
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")
        st.markdown("### Chat Information")
        st.markdown(f"Messages in conversation: {len(st.session_state.messages)}")
        st.markdown("---")
        st.markdown(
            """
            ### Tips
            - Be specific in your questions
            - Ask about oil and gas industry topics
            - You can clear the chat history anytime
            """
        )

if __name__ == "__main__":
    main()
