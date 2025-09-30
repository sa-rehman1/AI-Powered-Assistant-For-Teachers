import streamlit as st
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# LangChain Imports
# Note: Ensure you have the correct LangChain community imports for the latest structure
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, OpenAI, ChatOpenAI
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import PromptTemplate

# Function Name updated to align with README: counselor
def counselor():
    
    # 1. Secure API Key Loading
    if not OPENAI_KEY:
        st.error("OpenAI API Key not found. Please set it in your root .env file.")
        return

    # 2. Updated Vector DB Path
    persist_directory = 'data/vector_db/wellness_chroma'

    embedding = OpenAIEmbeddings(api_key=OPENAI_KEY)

    # Note: If the vectordb does not exist at this path, you will need to run your ingestion script first
    try:
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    except Exception as e:
        st.error(f"Error loading Vector Database from {persist_directory}. Please ensure it is built.")
        st.stop()


    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key = OPENAI_KEY)


    # st.markdown('<h1 style="font-family:Times New Roman;color:darkred;text-align:center;">AI Counsellor For Mental Wellness</h1>',unsafe_allow_html=True)
    st.markdown('<i><h3 style="font-family:Arial;color:darkred;text-align:center;font-size:20px;padding-left:50px">Chat with our AI Counsellor to seek help for your mental health</h3><i>',unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # Accept user input
    if prompt := st.chat_input("How may I help you!"):
    # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)


    # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, try to make up an answer but related to topic. Use three sentences maximum. Ask questions to get more better understanding of the problem. Be empathetic, understanding as you are dealing with teachers who want counselling.  
            {context}
            Question: {question}
            Helpful Answer:"""
            QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template)

            # Run chain
            qa_chain = RetrievalQA.from_chain_type(
                llm,
                retriever=vectordb.as_retriever(),
                chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
            )

            result = qa_chain({"query": prompt})

            # Simulate stream of response with milliseconds delay
            full_response += result["result"]
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.05)
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history

        st.session_state.messages.append({"role": "assistant", "content": full_response})