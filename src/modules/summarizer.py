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
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import PromptTemplate

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def summarize():
    if not OPENAI_KEY:
        st.error("OpenAI API Key not found. Please set it in your root .env file.")
        return

    # st.markdown('<h1 style="font-family:Lora;color:darkred;text-align:center;">Summarize Your Lesson</h1>',unsafe_allow_html=True)
    # st.markdown('<i><h3 style="font-family:Arial;color:darkred;text-align:center;font-size:20px;padding-left:50px">Your AI Assistant To Summarize Lessons To Help You Cover Bullet Points!</h3><i>',unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload PDF File Of Your Lesson")

    if uploaded_file:
        with st.spinner("Summarizing lesson into bullet points..."):
            
            # Save the file temporarily to load it
            temp_file_path = os.path.join("/tmp", uploaded_file.name) if os.name != 'nt' else uploaded_file.name
            with open(temp_file_path, mode='wb') as w:
                w.write(uploaded_file.getvalue())
            
            loader = PyPDFLoader(temp_file_path)
            pages = loader.load()
            
            # Split
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 1500,
                chunk_overlap = 150
            )

            splits = text_splitter.split_documents(pages)

            embedding = OpenAIEmbeddings(api_key=OPENAI_KEY)

            # Updated Vector DB Path
            persist_directory = 'data/vector_db/docs_chroma'

            # Note: This operation builds the vector database on upload, which might be slow.
            # If you want to use a pre-built one, change `from_documents` to a simple `Chroma()` call.
            vectordb = Chroma.from_documents(
                documents=splits,
                embedding=embedding,
                persist_directory=persist_directory
            )

            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key = OPENAI_KEY)
                            
            template = """Use the following pieces of context and summarize the whole lesson for the teacher in bullet point to help teachers understand lesson. If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep the answer as concise as possible.  
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

            result = qa_chain({"query": "Summarize this lesson for me. I am a teacher, I need to better understand this lesson. put it in bullet points"})

            st.success(result['result'])

            # Clean up the vector DB instance after use
            vectordb.delete_collection()
            
            # Clean up the temporary PDF file
            os.remove(temp_file_path)