import os
import json
import traceback
import pandas as pd
from src.mcqgenerator.utils import ReadFile,GetTableData
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging
import streamlit as st
from langchain.callbacks import get_openai_callback

with open(".\mcqgen\Response.json","r") as file:
    RESPONSE_JSON = json.load(file)
    
st.title('MCQs Creator Using Your data')

with st.form('User Input'):
    uploaded_file = st.file_uploader("Upload PDF or text file")
    
    mcq_count = st.number_input("No. of MCQs",min_value=3,max_value=50)
    
    subject = st.text_input("Inter Subject",max_chars=20)
    
    tone = st.text_input('Difficulty level of Questions',max_chars=20,placeholder='Simple')
    
    button = st.form_submit_button("Create MCQs")
    
    
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("In progress..."):
            try:
                text = ReadFile(uploaded_file)
                
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            'text':text,
                            'number':mcq_count,
                            'subject': subject,
                            'tone': tone,
                            'response': json.dumps(RESPONSE_JSON)
                        }
                    )
                    #st.erite(response)
                    
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("ERROR")
            else:
                print(f"Total Tokens{cb.total_tokens}")
                print(f"Prompt Tokens{cb.prompt_tokens}")   
                print(f"Completion Tokens{cb.completion_tokens}")   
                print(f"Total Cost{cb.total_cost}")
                
                if isinstance(response,dict):
                    quiz = response.get('quiz',None)
                    if quiz is not None:
                        table_data = GetTableData(quit)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index+1
                            st.table(df)
                            st.text_area(label='Review',value=response['review'])
                        else:
                            st.write(response)
                            
                                       
                