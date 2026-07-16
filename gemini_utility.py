import os
import json
import google.generativeai as genai
import streamlit as st

working_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(working_directory, "config.json")

# 1. Look for Streamlit Cloud Secrets first (Production environment)
if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)

# 2. Fall back to local file if secrets aren't there (Your Laptop environment)
elif os.path.exists(config_file_path):
    with open(config_file_path, "r") as file:
        config_data = json.load(file)
    GOOGLE_API_KEY = config_data.get("GOOGLE_API_KEY", "")
    if GOOGLE_API_KEY:
        genai.configure(api_key=GOOGLE_API_KEY)

def load_gemini_pro_model():
   
    gemini_pro_model = genai.GenerativeModel("gemini-2.5-flash-lite")
    return gemini_pro_model

def gemini_pro_vision_response(prompt, image):
   
    gemini_pro_vision_model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = gemini_pro_vision_model.generate_content([prompt, image])
    result = response.text
    return result

# function to get embedding text
def embedding_model_response(input_text):
    embedding_model = "models/gemini-embedding-001" 
    
    embedding = genai.embed_content(
        model=embedding_model,
        content=input_text,
        task_type="retrieval_document"
    )
    
    embedding_list = embedding["embedding"]
    return embedding_list

# function to get response from gemini pro from llm
def gemini_pro_response(user_prompt):
 
    gemini_pro_model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result
