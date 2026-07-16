import os
import sys
import importlib  # Built-in tool to force clear module caches
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu

# --- FORCE CACHE FLUSH FOR ONEDRIVE ---
import gemini_utility as gu
importlib.reload(gu)  # This destroys the old cache and forces a fresh load!
# --------------------------------------

working_directory = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Geminiai",
    page_icon="👽",
    layout="centered"
)

with st.sidebar:
    selected = option_menu("Gemini ai",
                           ["Chatbot",
                            "Image captionong",
                            "Embedded Text",
                            "Ask me anything"],
                           menu_icon="robot",
                           icons=["chat-dots-fill",
                                  "image",
                                  "card-text",
                                  "question-circle"],
                           default_index=0
                           )

# function to translate role between gemini pro and streamlit terminology
def translate_role_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    
if selected == "Chatbot":
    model = gu.load_gemini_pro_model()

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    st.title("🤖 Chatbot")

    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    user_prompt = st.chat_input("Ask me anything")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        
        # --- FIXED: Added try-except to catch 429 errors ---
        try:
            gemini_response = st.session_state.chat_session.send_message(user_prompt)
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text)
        except Exception as e:
            with st.chat_message("assistant"):
                st.error(
                    "⚠️ Quota Exceeded / Too Many Requests. The free tier limits requests to 20 per window. "
                    "Please wait about 60 seconds before trying again, or upgrade your billing tier."
                )


# image section
# image section
if selected == "Image captionong":
    st.title=("🖼️ Image captionong")
    
    if "image_caption" not in st.session_state:
        st.session_state.image_caption = ""

    uploaded_image = st.file_uploader("upload image her...", type=["jpeg", "png", "jpg"])
    
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        col1, col2 = st.columns(2)

        with col1:
            resize_image = image.resize((800, 500))
            st.image(resize_image)
            
        if st.button("generate caption"):
            with st.spinner("Generating caption..."):
                default_prompt = "write a short caption for this image"
                st.session_state.image_caption = gu.gemini_pro_vision_response(default_prompt, image)

        if st.session_state.image_caption:
            with col2:
                st.info(st.session_state.image_caption)
#text embedding

if selected == "Embedded Text":
    st.title("💬 Embedding Text")

    input_text = st.text_area(label="", placeholder="enter the text to get embeddings")
    
    if st.button("get embedding"):
        if not input_text.strip():
            st.warning("Please type some text into the box first!")
        else:
            with st.spinner("Generating embedding vector..."):
                try:
                    response = gu.embedding_model_response(input_text)
                    st.success("Embedding generated successfully!")
                    st.code(str(response))
                except Exception as e:
                    st.error(f"API Error: {e}")

#ask me anyhting
if selected == "Ask me anything":
    st.title("❓ ask me anything")

    user_prompt=st.text_area(label="",placeholder="ask gemini pro")
    if st.button("get response"):
        if not user_prompt.strip():
            st.warning("please ask gemini pro")
        else:
            with st.spinner("generating response"):
                try:
                    response=gu.gemini_pro_response(user_prompt)
                    st.success("generated successfully ")
                    st.code(str(response))
                except Exception as e:
                    st.error(f"API Error: {e}")