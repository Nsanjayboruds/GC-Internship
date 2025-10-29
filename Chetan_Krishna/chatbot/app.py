import utils.session
import streamlit as st
import requests
import json
import time

# Function to simulate an API request (dummy function)
def update_request(company_name, esg_link, annual_report_link):
    url = 'http://127.0.0.1:3000/update'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    data = {
        "company_name": company_name,
        "esg_link": esg_link,
        "annual_report_link": annual_report_link
    }

    res = requests.put(url, headers=headers, data=json.dumps(data))

    return res.json()

def execute_query_request(query):
    url = 'http://127.0.0.1:3000/execute-query'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    data = {
        'query': query
    }

    res = requests.post(url, headers=headers, data=json.dumps(data))

    return res.json()

def chat_request(user_input):
    url = 'http://127.0.0.1:3000/chat'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    data = {
        'prompt': user_input
    }

    res = requests.post(url, headers=headers, data=json.dumps(data))

    return res.json()

st.set_page_config(page_title="Company Universe", page_icon="📄", layout="centered")

st.markdown(f"""<style>.stContainer {{
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 300px;
                z-index: 1000;
            }}
            </style>""", 
            unsafe_allow_html=True)

# Streamlit app layout
st.title("Company Universe")

# Input fields
company_name = st.text_input("Company Name")
esg_link = st.text_input("ESG Link" )
annual_report_link = st.text_input("Annual Report Link")

# Submit button
if st.button("Submit"):
    all_fields_filled = company_name and (esg_link or annual_report_link)
    if(all_fields_filled):
        print("Making API request...")
        print(f"Company Name: {company_name}, ESG Link: {esg_link}, Annual Report Link: {annual_report_link}")
        result = update_request(company_name, esg_link, annual_report_link)
        # Display the result
        if result["status"] == "success":
            st.success(result["data"], icon="✅")
        else:
            st.error(result["data"], icon="❌")
    else:
        st.warning("Please fill all the fields", icon="⚠️")
        
# Query input field
query = st.text_input("Enter your query here")
st.text("Example: SELECT `Company`, `Company annual reports page URL`,  `Company sustainability / ESG reports page URL`  FROM company_universe LIMIT 10;")
# Query submit button
if st.button("Execute Query"):
    if query:
        result = execute_query_request(query)
        if result["status"] == "success":
            st.success("Query executed successfully", icon="✅")
            st.dataframe(result["data"])
        else:
            st.error(result["data"], icon="❌")
    else:
        st.warning("Please enter a query", icon="⚠️")
        
with st.container():
    user_input = st.text_input("Ask a question:", key="chat_input", placeholder="Type your question here...")
    if st.button("Send", key="send_button"):
       
        with st.spinner('Waiting for response...'):
            response = chat_request(user_input)
            
        if(response["status"] == "success"):
            st.text_area("Response:", value=response["data"], height=100, key="response_area", disabled=True)
        else:
            st.error(result["data"], icon="❌")

