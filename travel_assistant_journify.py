import streamlit as st
import os
import openai
from io import StringIO
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
import pandas as pd
from rapidfuzz import fuzz, process
from streamlit_chat import message
from streamlit.components.v1 import html
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts import PromptTemplate
from langchain import LLMChain

load_dotenv()
#side bar contents
with st.sidebar:
    st.title('🤗💬 LLM Chat App')
    st.image('mag.jpg')
    st.markdown("""
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [Langchain](https://python.langchian.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
    - [Github](https://github.com/praj2408/Langchain-PDF-App-GUI) Repository
                
    """)
    # add_vertical_space(5)
    st.write("By MAG.")

def main(prompt):
    st.header("Chat with Me 💬")
    input_container = st.container()
    response_container = st.container()
    
    reset_button_key = "reset_button"
    reset_button = st.button("Clear Chat",key=reset_button_key)
    if reset_button:
        st.session_state['user_responses'] = []
        st.session_state['bot_responses'] = []

    if 'user_responses' not in st.session_state:
        st.session_state['user_responses'] = ["Hey"]
    if 'bot_responses' not in st.session_state:
        st.session_state['bot_responses'] = ["Hey there! How may I help you today?"]

    #                          ^^^   <--- here
    # st.write(query)
    # Accept user questions/query
    query = st.text_input("Ask questions", placeholder="Type your question here")
    # Initialize session state variables
    with response_container:
        if query:
            model_name = os.getenv('MODEL_NAME')
            api_key = os.getenv('OPENAI_API_KEY')

            llm = OpenAI(model_name=model_name,engine=model_name)
            # example_prompt = PromptTemplate(input_variables=['input'],template=prompt)
            memory = ConversationBufferMemory(memory_key="chat_history")
            # Initiate a connection to the LLM from Azure OpenAI Service via LangChain.
            # chain = LLMChain(llm=llm, prompt = example_prompt)
            chain = LLMChain(llm=llm, prompt=prompt, memory = memory)
            response = chain.run(query)
            # response = agent.run(query)
            st.session_state.user_responses.append(query)
            st.session_state.bot_responses.append(response)           
        if st.session_state['bot_responses']:
            for i in range(len(st.session_state['bot_responses'])):
                message(st.session_state['user_responses'][i], is_user=True, key=str(i) + '_user', avatar_style="initials", seed="Kavita")
                message(st.session_state['bot_responses'][i], key=str(i), avatar_style="initials", seed="AI",)
    with input_container:
        display_input = query

if __name__ == "__main__":

    dotenv_path = '/Workspace/Users/karlok.soo@malaysiaairlines.com/.env'
    load_dotenv(dotenv_path)
    openai.api_key = os.getenv('OPENAI_API_KEY')
    model_name = os.getenv('MODEL_NAME')
    openai.api_type = os.getenv('OPENAI_API_TYPE')
    openai.api_base = os.getenv('OPENAI_API_BASE')
    openai.api_version = os.getenv('OPENAI_API_VERSION')
    serp_api = os.getenv('SERPAPI_API_KEY')

    developer_template = """

    You are a helpful travel assistant from Journify. Your only task is to help user to get the travel information from Journify website that hosted by malaysia airlines. 
    Based on users requirements answer and provide the specific website link of Journify that fit and suit the user's needs.
    For example, if user say would like to go genting, you may show genting themepark ticket in Journify "https://shop.myjournify.com/products/genting-skyworld-outdoor-theme-park-82647" or 
    genting highland tour in Journify "https://shop.myjournify.com/products/genting-highlands-tour-87751".
    Please suggest the attarctions to the users.

    If the information could not found from Journify website.  
    Respond with just 'sorry, we dont have the information in Journify'.
     
    {chat_history}
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(developer_template)
    human_template="{query}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt,human_message_prompt])

    main(chat_prompt)