from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import gradio as gr

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input, image):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, image[0]])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


input_prompt = """
As an experienced certified personal trainer and healthcare professional, your expertise is needed to evaluate the form and posture in the provided image for the {Exercise}.
Please assess whether the form is correct.  
If the form is incorrect, offer corrective advice in bullet points.
"""

st.set_page_config(page_title="Form checker App")

st.header("Form checker")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    input = st.text_input("Enter Exercise Name: ", key="input")

submit = st.button("check my form")
if submit:
    image_data = input_image_setup(uploaded_file)
    complete_prompt = input_prompt.format(Exercise=input)
    response = get_gemini_response(
        complete_prompt,
        image_data,
    )
    st.subheader("The Response is")
    st.write(response)
