import os
import json
import google.generativeai as genai
import streamlit as st

working_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(working_directory, "config.json")

GOOGLE_API_KEY = None

# 1. Safely check if Streamlit Secrets exist first (Cloud Environment)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

# 2. Fallback to your local config.json file (Laptop Environment)
if not GOOGLE_API_KEY and os.path.exists(config_file_path):
    with open(config_file_path, "r") as file:
        config_data = json.load(file)
    GOOGLE_API_KEY = config_data.get("GOOGLE_API_KEY", "")

# 3. Apply the key configuration if found
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    st.error("⚠️ API Key is missing!")

def load_gemini_pro_model():
    return genai.GenerativeModel("gemini-2.5-flash")

def gemini_pro_vision_response(prompt, image):
    # FIXED: Uses standard active flash model to process images
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([prompt, image])
    return response.text

def embedding_model_response(input_text):
    embedding = genai.embed_content(
        model="models/text-embedding-004",
        content=input_text,
        task_type="retrieval_document"
    )
    return embedding["embedding"]

def gemini_pro_response(user_prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(user_prompt)
    return response.text
