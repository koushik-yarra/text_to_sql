import streamlit as st
import os
import sqlite3

import google.generativeai as genai
## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

from dotenv import load_dotenv
load_dotenv() ## load all the environment variables

## Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-2.0-flash')
    response=model.generate_content([prompt[0],question])
    return response.text

## Function To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt=[
    """
    You are an expert AI assistant specializing in converting natural language questions into SQL queries. 

### Database Schema:
The database is named **STUDENT** and contains the following columns:
- **ID** (INTEGER) - Unique identifier for each student
- **NAME** (TEXT) - Student's full name
- **CLASS** (TEXT) - The grade or class of the student (e.g., "10TH", "9TH")
- **SECTION** (TEXT) - The section in which the student is enrolled (e.g., "A", "B")

### Instructions:
- Convert the given English question into a valid **SQLite SQL query**.
- Ensure the SQL query is **correctly formatted**, optimized, and executable.
- The query should return relevant results based on the database schema.
- **Do not** include any additional explanation, only return the SQL query.
- **Do not** enclose the query in triple backticks (` ``` `) or prepend it with "sql".
- If the question is unclear or lacks necessary details, assume reasonable defaults.

### Examples:
1. **Question:** "How many students are in the database?"  
   **SQL Query:** `SELECT COUNT(*) FROM STUDENT;`

2. **Question:** "Show all students in class 10TH, section A."  
   **SQL Query:** `SELECT * FROM STUDENT WHERE CLASS = '10TH' AND SECTION = 'A';`

3. **Question:** "List the names of all students sorted alphabetically."  
   **SQL Query:** `SELECT NAME FROM STUDENT ORDER BY NAME ASC;`

4. **Question:** "Find the student with ID 5."  
   **SQL Query:** `SELECT * FROM STUDENT WHERE ID = 5;
    """


]

## Streamlit App

st.set_page_config(page_title="SQL BOT", page_icon=":guardsman:", layout="wide")
st.title("TEXT TO SQL ")
st.subheader("Ask your question in English and get SQL query as response")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"student.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)