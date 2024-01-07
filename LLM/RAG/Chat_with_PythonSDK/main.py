import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from chat_chain import SDKChat

st.set_page_config(page_title="Chat with IBM Generative AI Python SDK", page_icon="🖖")
st.title("🖖 Chat with IBM Generative AI Python SDK")

# ------ INIT ------
@st.cache_resource
def init_chat():
    # Set up memory
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    memory = ConversationBufferMemory(chat_memory=msgs)

    # create a chat instance
    sdk_chat = SDKChat(debug=True,json_logging=True)
    sdk_chat.create_chat()
    return sdk_chat, msgs

sdk_chat, msgs = init_chat()

if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    # write question to UI and history
    st.chat_message("human").write(prompt)
    msgs.add_user_message(prompt)

    # generate response
    response = sdk_chat.invoke({'chat_history': msgs.messages, 'question': prompt})

    # write response to UI and history
    st.chat_message("ai").write(response)
    msgs.add_ai_message(response)