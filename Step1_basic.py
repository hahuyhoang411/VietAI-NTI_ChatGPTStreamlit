import streamlit as st
import openai

# Custom Streamlit app title and icon
st.set_page_config(
    page_title="VietAI Bot",
    page_icon=":robot_face:",
)

st.title("[VietAI-NTI] ChatGPT")

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# '''
# st.session_state is a feature provided by Streamlit that allows you to store
# and access data persistently across different interactions
# within a Streamlit app. It's a way to maintain state information between
# different user interactions without the need for complex workarounds or
# external storage.
# '''

# Set a default model
# '''
# This code checks if the OpenAI model to be used is already stored in Streamlit's session state.
# If not, it sets the default model to "gpt-3.5-turbo".
# You can switch to "gpt-4" for better results.
# '''

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
# '''
# This code initializes an empty list to store chat messages
# in Streamlit's session state if it doesn't already exist.
# '''

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
# '''
# This loop iterates through the stored chat messages and displays them in the chat interface.
# It uses Streamlit's st.chat_message and st.markdown to format and display the messages.
# '''
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
# '''
# This section handles user input and AI responses.
# It checks if the user has entered a message using st.chat_input.
# If a user message is provided, it appends the user's message to the chat history in Streamlit's session state and displays it in the chat interface.
# It then uses the OpenAI API to generate an AI response based on the user's input.
# As the AI generates responses in a streaming fashion (character by character), it updates the chat interface in real-time using st.empty() and st.markdown. The AI's responses are gradually displayed as they are generated.
# Finally, the AI's full response is stored in the chat history.
# '''
if prompt := st.chat_input("Bạn cần hỗ trợ điều gì?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})