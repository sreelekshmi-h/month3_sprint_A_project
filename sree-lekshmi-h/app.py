import streamlit as st
from groq import RateLimitError
from agents import handle_query


st.set_page_config(
    page_title="Novi-AI Personal Assistant",
    page_icon="🤖"
)

st.title("🤖 Novi-Your AI Personal Assistant")
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
    st.chat_message("user").write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                answer = handle_query(
                    user_input,
                    st.session_state.messages
                )

            st.write(answer)

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

            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message,
                "error": True
            })



        except Exception as e:
            st.error(f"Error: {type(e).__name__}: {e}")
            st.exception(e)
