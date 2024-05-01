import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from st_social_media_links import SocialMediaIcons

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro')

if "Chat_history" not in st.session_state:
    st.session_state["Chat_history"] = []


def get_gemini_response(input_text, input_prompt):
    response = model.generate_content([input_text, input_prompt])
    return response.text


st.set_page_config(page_title='Medicine_Query_From_Medicine_Name', page_icon='icon_home.png')
with open('design.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.header("Identify Medicines by Name 🔎")
st.sidebar.success("Select a Page")
st.write('----')
st.image('bg_mqn.png')
st.write('----')
input_prompt = """
You are a doctor, whenever user write a medicine name, tell the name of the medicine, for which diseases this medicine preferred,
which age people should use this medicine and what are the components of the medicine,
According the below format:
1. Medicine Name:
(New line) 2. For What Diseases It Preferred:
(New line) 3.Who Should Use: based on age and mention age
(New line) 4.Components of the Medicine:
write Medicine name h3 format, For What Diseases It Preferred, Who Should Use, Components of the Medicine in h5 format
"""

input_text = st.text_area("**Write a medicine name Here**", key='input_text')
submit = st.button("**Tell About this Medicine**")
chat_history_key = st.button("**Chat History**")
st.write('----')
if len(input_text) > 0 and submit:
    with st.spinner("**Generating...**"):
        response = get_gemini_response(input_text=input_text, input_prompt=input_prompt)
        st.write(response)
        st.session_state["Chat_history"].append({"user": input_text, "response": response})
        st.write("**Tell How Well Our App is! We are very excited to Know 🙃**")
        rating = st.slider('**Rate our app:**', 1, 5, 1)
        st.write(f'You rated the app {rating} out of 5.')
        if rating:
            st.write("Very Very Thanks for your review! 😍")
elif len(input_text) <= 0 and submit:
    st.write("**Write a Medicine Name! 💊**")


if chat_history_key:
    if st.session_state["Chat_history"] != None:
        for chat in st.session_state["Chat_history"]:
            st.write(f"**You:** {chat['user']}")
            st.write(f"**Dr. Health AIly:** {chat['response']}")