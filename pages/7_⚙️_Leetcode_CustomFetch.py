import streamlit as st
import pandas as pd
from Endpoints import returnQuery

st.write('# **Custom Data Fetch**')

file = st.file_uploader("Upload your file here")

st.write(' The Csv file should contain Name ,  Username , Reg Number,Year,Domain , Section , Department , Mail ID , Mobile Number')

if file:

    df = pd.read_csv(file)

    data = []
    error_fetching = []

    for ind, row in df.iterrows():
        name = str(row['Name']).strip()
        regno = str(row['Reg Number']).strip()
        year = str(row['Year']).strip()
        dept = str(row['Department']).strip()
        section = str(row['Section']).strip()
        domain = str(row['Domain']).strip()
        mail = str(row['Mail ID']).strip()
        phone = str(row['Mobile Number']).strip()
        user = str(row['Username']).strip()
        
        problemsDict, flag = returnQuery(user, name, regno, year, dept, section, domain, mail, phone)
        
        if flag:
            data.append(problemsDict)
        else:
            error_fetching.append(problemsDict)
            print(f'{user} not found')

    

    if data:    
        dataframe = pd.DataFrame(data)
        dataframe.set_index('Name', inplace=True)
        
    if error_fetching:
        error = pd.DataFrame(error_fetching)
        error.set_index('Name', inplace=True)
        st.write('## **Failed to Fetch**')
        st.write(error)
    
    if data:
        st.session_state['data'] = dataframe
        st.write(st.session_state.get('data'))
    
        


    
if  not file:
    st.session_state['data'] = pd.DataFrame()