import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from st_social_media_links import SocialMediaIcons


load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model = genai.GenerativeModel('gemini-pro')


def get_gemini_response(input_text, input_prompt):
    response = model.generate_content([input_text, input_prompt])
    return response.text


st.set_page_config(page_title="Dr. Health AIly", page_icon='icon_home.png')
if "Chat_history" not in st.session_state:
    st.session_state["Chat_history"] = []

with open('design.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.sidebar.success("Select a page")
st.title("Welcome to Dr. Health AIly 🩺")
st.write('----')
st.image('bg_Home.png')
st.write('----')
input_prompt = """
You are a doctor so whenever user write a list of ailments user realizing, You have to identify what the sickness/disease and 
You will prefer medicines and offer advice like what precautions should user take overcoming the sickness/disease
and also suggest healthy foods user should consume to cure and also guide 
user how to stay fit and healthy daily so that the ailments would not occur user again.
In the following format:
Disease Name:
Preferred Medicine: Categories medicines based on age
Precautions Should Taken:
Preferred Food:
How to Stay Healthy:
write Disease Name,  Preferred Medicine, Preferred Food, How to Stay Healthy in h2 format
"""

input_text = st.text_area("**Enter a comma-separated symptoms/ailments:**")
submit = st.button("**Generate**")
chat_history_key = st.button("**Chat History**")
st.write("---")

if len(input_text) > 0 and submit:
    with st.spinner("**Generating...**"):
        response = get_gemini_response(input_text=input_text, input_prompt=input_prompt)
        st.write(response)
        st.session_state["Chat_history"].append({"user": input_text, "response": response})
        rating = st.slider('**Rate our App:**', 1, 5, 1)
        st.write(f'You rated the app {rating} out of 5.')
if len(input_text) <= 0 and submit:
    st.write("**Write Health issues !**")

if chat_history_key:
    if st.session_state["Chat_history"] != None:
        for chat in st.session_state["Chat_history"]:
            st.write(f"**You:** {chat['user']}")
            st.write(f"**Dr. Health AIly:** {chat['response']}")