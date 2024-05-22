import json
import traceback
import pandas as pd
from src.mcqgenerator.utils import ReadFile, GetTableData
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging
import streamlit as st

# Load the RESPONSE_JSON
with open("D:\\DSProjects\\mcqgen\\Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

st.title('MCQs Creator Using Your Data')

# User input form
with st.form('User Input'):
    uploaded_file = st.file_uploader("Upload PDF or text file")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Enter Subject", max_chars=20)
    tone = st.text_input('Difficulty level of Questions', max_chars=20, placeholder='Simple')
    button = st.form_submit_button("Create MCQs")

    # Check if the form is submitted and all inputs are provided
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("In progress..."):
            try:
                # Read the content of the uploaded file
                text = ReadFile(uploaded_file)

                # Generate MCQs
                response = generate_evaluate_chain.invoke({
                    'text': text,
                    'number': mcq_count,
                    'subject': subject,
                    'tone': tone,
                    'response_json': json.dumps(RESPONSE_JSON)
                })

                # Check if response is a dictionary
                if isinstance(response, dict):
                    quiz = response.get('quiz', None)
                    if quiz:
                        table_data = GetTableData(json.dumps(quiz))
                        if table_data:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label='Review', value=response.get('review', ''))
                        else:
                            st.write(response)
                    else:
                        st.write(response)
                else:
                    st.error("Unexpected response format.")
                    
            except Exception as e:
                # Handle any exceptions that occur during processing
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("An error occurred during the process. Please check the console for details.")
