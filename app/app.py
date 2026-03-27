import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
import os
import dotenv ;dotenv.load_dotenv()
st.set_page_config('Restructuring Agent',	
':shamrock:',layout='wide')
st.markdown('<h1 style="color: white;">🧠 Data Extraction Chatbot</h1>',unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1503264116251-35a269479413");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.write('<h5 style="color :white ;">Paste any messy or unstructured text (receipts, notes, or transcriptions), and get a clean Python dictionary.</h5>',unsafe_allow_html=True)

st.write('<h5 style="color : white ;">Returns only structured data</h5>',unsafe_allow_html=True)
st.write('<h5 style="color:white;">Automatically detects fields (date, items, total, etc.)</h5>',unsafe_allow_html=True)
st.write('<h5 style="color : white;">Handles missing or uncertain values</h5>',unsafe_allow_html=True)
st.write('<h5 style="color : white;">Normalizes numbers and formats output</h5>',unsafe_allow_html=True)
st.write('<h5 style="color : white;">Enter your text below 👇</h5',unsafe_allow_html=True)

client = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url="https://api.groq.com/openai/v1",
)


unstructured_text=st.text_area('Paste your Unstructured text here')

prompt="""You are an intelligent data extraction system.

Your task is to convert any unstructured text into clean, structured JSON.

Instructions:
- Detect the type of document automatically (e.g., receipt, invoice, medical record, shipment, etc.).
- Extract all relevant entities and organize them into a logical JSON structure.
- Create appropriate field names dynamically based on the content.
- Group related data (e.g., items in a list, vitals in an object, etc.).

Normalization Rules:
- Dates → YYYY-MM-DD
- Numbers → numeric only (no currency symbols or text)
- Booleans → true/false
- Missing or unclear values → null

Strict Rules:
- Output ONLY valid JSON.
- Do NOT include explanations or extra text.
- Do NOT hallucinate unknown values.
- Keep structure clean and readable.

Output Guidelines:
- Use nested objects where appropriate.
- Use arrays for repeated elements (e.g., items, medications).
- Keep naming consistent and meaningful.
Return only JSON"""

@st.dialog("Structured Output")
def show_result(result):
    st.code(result)  # أو st.code لو string

if st.button('Apply'):
    response = client.responses.create(
        model="openai/gpt-oss-20b",
        input=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": unstructured_text}
        ],
    )

    result = response.output_text
    show_result(result)

