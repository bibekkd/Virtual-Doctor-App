import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
from st_social_media_links import SocialMediaIcons

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        images_parts = [
            {
                "mime_type" : uploaded_file.type,
                "data": bytes_data
            }
        ]
        return images_parts
    else:
        raise FileNotFoundError("No file uploaded, so far :(")


st.set_page_config(page_title="Medicine Query From Image", page_icon='icon_home.png')
with open('design.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.sidebar.success("Select a page")
st.subheader("Medicine Identification through Images 💊")
st.write('----')
st.image('bg_mqi.png')
st.write('----')
uploaded_file = st.file_uploader("**Choose a Medicine Image...**", type=['jpg', 'jpeg', 'png'])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

submit = st.button("**Tell About This Medicine**")
st.write('----')
input_prompt = """
You are a doctor, whenever user upload a medicine image, tell the name of the medicine, for which diseases this medicine preferred,
which age people should use this medicine and what are the components of the medicine,
According the below format:
1. Medicine Name
(New line) 2. For What Diseases It Preferred
(New line) 3.Who Should Use: (based on age and mention age) 
(New line) 4.Components of the Medicine
write Medicine name h3 format, For What Diseases It Preferred, Who Should Use, Components of the Medicine in h5 format
"""

if submit:
    with st.spinner("**Generating..**"):
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt=input_prompt, image=image_data)
        st.write(response)
        rating = st.slider('**Rate our App:**', 1, 5, 1)
        st.write(f'You rated the app {rating} out of 5.')

