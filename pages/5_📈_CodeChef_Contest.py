import streamlit as st
import pandas as pd
from Endpoints import codechef_contest

st.write('# **CodeChef Contest Data Fetch**')

contestName = st.text_input("Enter the name of the contest:")

if contestName:

    file = pd.read_csv('./data/model.csv')
    filtered_data = file.copy()
        
    departments = ["All"] + list(file['Department'].unique())
    sections = ["All"] + list(file['Section'].unique())
    years = ["All"] + list(file['Year'].unique())
    domains = ["All"] + list(file['Domain'].unique())

    year = st.selectbox('Year', years, index=0)
    department = st.selectbox('Department', departments, index=0)
    domain = st.selectbox('Domain', domains, index=0)
    section = st.selectbox('Section' , sections, index=0)


    if year:
        if year != 'All':
            filtered_data = filtered_data[filtered_data['Year'] == year]

    if department:
        if department != 'All':
            filtered_data = filtered_data[filtered_data['Department'] == department]
        
    if section:
        if section != 'All':
            filtered_data = filtered_data[filtered_data['Section'] == section]
                    
    if domain:
        if domain != 'All':
            filtered_data = filtered_data[filtered_data['Domain'] == domain]


    if st.button('Fetch'):
        df = filtered_data
    
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

            user = str(row['CODECHEF ID']).strip()
            
            problemsDict, flag = codechef_contest(user,contestName)
            
            if flag:
                problemsDict['Name'] = name
                regno = str(row['Reg Number']).strip()
                year = str(row['Year']).strip()
                dept = str(row['Department']).strip()
                section = str(row['Section']).strip()
                domain = str(row['Domain']).strip()
                mail = str(row['Mail ID']).strip()
                phone = str(row['Mobile Number']).strip()

                data.append(problemsDict)
            else:
                problemsDict['Name'] = name
                regno = str(row['Reg Number']).strip()
                year = str(row['Year']).strip()
                dept = str(row['Department']).strip()
                section = str(row['Section']).strip()
                domain = str(row['Domain']).strip()
                mail = str(row['Mail ID']).strip()
                phone = str(row['Mobile Number']).strip()
                
                error_fetching.append(problemsDict)
               
      

        dataframe = pd.DataFrame()
        
        if data:    
            dataframe = pd.DataFrame(data)
            dataframe.set_index('Name', inplace=True)
            
        if error_fetching:
            error = pd.DataFrame(error_fetching)
            st.write('## **Failed to Fetch**')
            st.write(error)
        
        
        st.session_state['data'] = dataframe
        st.write(st.session_state.get('data'))