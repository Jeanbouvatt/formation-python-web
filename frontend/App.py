import streamlit as st
import requests


st.header("""Postez un message""")
with st.form("my_form"):
    author = st.text_input("Nom")
    message = st.text_area("Message")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        requests.post(f"http://127.0.0.1:8000/messages/", json={
          "author": author,
          "message": message
        })
## current messages
response = requests.get(f"http://127.0.0.1:8000/messages/")
for message in response.json():
    st.header(message['author'])
    st.write(message['message'])
