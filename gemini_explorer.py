import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, ChatSession

# Initialize Vertex AI project
project = 'robust-flow-436500-q3'
vertexai.init(project=project)

# Set the model configuration
config = generative_models.GenerationConfig(
    temperature=0.4
)

# Load the Gemini Pro model with the configuration
model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)

# Start a chat session with the model
chat = model.start_chat()

# Helper function to handle chat responses
def llm_function(chat: ChatSession, query):
    # Send the user's query to the model and get the response
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    # Display model response in Streamlit
    with st.chat_message("model"):
        st.markdown(output)

    # Append the messages to session state for chat history
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })
    st.session_state.messages.append({
        "role": "model",
        "content": output
    })

# Title of the Streamlit app
st.title("RadicalX Gemini Explorer")

# Initialize chat history and set an initial prompt flag in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "initial_prompt_sent" not in st.session_state:
    st.session_state.initial_prompt_sent = False

# Check if chat history is empty, and if so, send initial prompt only once
if not st.session_state.initial_prompt_sent:
    initial_prompt = "Ahoy! I be ReX, yer assistant powered by Google Gemini! Ready to set sail on a quest for knowledge?"
    # Directly append the initial prompt without calling llm_function
    st.session_state.messages.append({
        "role": "model",
        "content": initial_prompt
    })
    st.session_state.initial_prompt_sent = True

# Display chat history in Streamlit
for message in st.session_state.messages:
    role = message['role']
    content = message['content']

    with st.chat_message(role):
        st.markdown(content)

# Capture user input from the Streamlit chat input widget
query = st.chat_input("Message ReX")

# Process user's input and get model's response
if query:
    with st.chat_message("user"):
        st.markdown(query)

    llm_function(chat, query)

