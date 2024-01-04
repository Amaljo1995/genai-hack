import streamlit as _st
from utils.Utils import extract_information
import os

_st.title("TechCrafters")
with _st.form("application"):
    resume      = _st.file_uploader("Insert your Updated Resume",type=['doc','docx','pdf'])
    description = _st.text_area("Job description",height=200)
    submitted   = _st.form_submit_button("Apply")
    if submitted:
        if resume is None or description.strip() == "":
            _st.warning("Please fill all items")
        else:
            filePath = f'tempfiles/{resume.name}'
            with open(filePath,"wb") as temp:
                temp.write(resume.getvalue())
            _st.session_state.file = filePath
            _st.session_state.parsedResume = extract_information(filePath)
            _st.session_state.description  = description.strip()
            _st.success("Submitted successfully")
            print("dss")