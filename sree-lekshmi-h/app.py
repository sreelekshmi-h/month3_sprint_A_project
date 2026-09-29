import streamlit as st
from groq import RateLimitError
from agents import handle_query

st.set_page_config(
    page_title="AI Personal Assistant",
    page_icon="🤖"
)

st.title("🤖 AI Personal Assistant")
st.write("Ask questions, perform calculations, or get researched information.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("error"):
            st.warning(message["content"])
        else:
            st.write(message["content"])

# User input
user_input = st.chat_input("Ask me something...")

if user_input:

    # Show user message
    with st.chat_message("user"):
        st.write(user_input)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Generate response
    with st.chat_message("assistant"):

        try:
            with st.spinner("Thinking..."):
                answer = handle_query(user_input)

            st.write(answer)

            # Save normal response
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except RateLimitError:
            error_message = (
                "⚠️ Groq API rate limit reached. "
                "Please wait and try again later."
            )

            st.warning(error_message)

            # Save error only after a query was submitted
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message,
                "error": True
            })

        except Exception as e:
            print(f"[ERROR] {e}")

            error_message = (
                "⚠️ Something went wrong while processing "
                "your request. Please try again."
            )

            st.warning(error_message)

            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message,
                "error": True
            })