import google.generativeai as genai
import streamlit as st


# App title
st.set_page_config(page_title="🤗💬 CHATBOT CAPSTON")

# Hugging Face Credentials
with st.sidebar:
    st.title('🤗💬 CHATBOT CAPSTON')
    reset_button_key = "reset_button"
    reset_button = st.button("Reset Chat", key=reset_button_key)
    if reset_button:
        # Reset the chat messages
        st.session_state.messages.clear()

# Display chat messages
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

if st.session_state.messages:  # Check if messages list is not empty
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt_input):
    # Hugging Face Login
    genai.configure(api_key='AIzaSyC163y1FrQbkllasUcnIk9_zyVlLkYAtRY')
    model = genai.GenerativeModel('gemini-pro')
    # Create ChatBot                        
    chatbot = model.generate_content(prompt_input)
    
    response_text = None
    
    # Iterate over chatbot.parts to find the part containing text
    for part in chatbot.parts:
        if hasattr(part, 'text'):
            response_text = part.text
            break

    # Check if response_text is still None
    if response_text is None:
        return "Sorry, I couldn't generate a response."
    else:
        return response_text

# User-provided prompt
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if there are messages and the last message is not from the assistant
if st.session_state.messages and st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
