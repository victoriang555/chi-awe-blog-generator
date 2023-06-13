from langchain import PromptTemplate, FewShotPromptTemplate 
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.llms import OpenAI
from dotenv import load_dotenv
from langchain.prompts.example_selector import LengthBasedExampleSelector
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import LLMChain, ConversationChain, SimpleSequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate

# Streamlit is the host for this app
# The following code is based on this example https://blog.streamlit.io/langchain-tutorial-2-build-a-blog-outline-generator-app-in-25-lines-of-code/ 
st.set_page_config(page_title ="Chi-AWE Blog Post Generator App")
st.title('Chi-AWE Blog Post Generator App')
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

def generate_response(topic):
  llm = OpenAI(model_name='text-curie-001', openai_api_key=openai_api_key)
  # Prompt
  template = 'As a AAPI woman interested in empowering other women and making friends in Chicagoland, generate a blog for a blog about {topic}.'
  prompt = PromptTemplate(input_variables=['topic'], template=template)
  prompt_query = prompt.format(topic=topic)
  # Run LLM model and print out response
  response = llm(prompt_query)
  return st.info(response)

with st.form('myform'):
  topic = st.text_input('Enter keyword:', '')
  submitted = st.form_submit_button('Submit')
  # Smoke test for whether the user is providing a valid OpenAi API Key
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
    generate_response(topic)