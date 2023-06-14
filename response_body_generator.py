import constants

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
from langchain.llms import OpenAI
from langchain import PromptTemplate

import streamlit as st

class ResponseBodyGenerator:
    def __init__(self, openai_api_key, person, topic): 
        self.openai_api_key = openai_api_key
        self.person = person
        self.topic = topic
        self.llm = OpenAI(model_name=constants.MODEL_NAME, openai_api_key=openai_api_key)
    
    def opening_paragraph_chain(self):
       """Generate the opening paragraph chain"""
       opening_paragraph_prompt = PromptTemplate(
            input_variables=[constants.PERSON, constants.TOPIC],
            template=constants.OPENING_PARAGRAPH_TEMPLATE
            )
    #    prompt_query = opening_paragraph_prompt.format(person=self.person, topic=self.topic)
       opening_paragraph_chain = LLMChain(llm=self.llm, prompt=opening_paragraph_prompt)
       return opening_paragraph_chain

    def second_paragraph_chain(self):
       """Generate the opening paragraph chain"""
       second_paragraph_prompt = PromptTemplate(
            input_variables=[constants.PERSON, constants.TOPIC],
            template=constants.SECOND_PARAGRAPH_TEMPLATE
            )
    #    prompt_query = second_paragraph_prompt.format(person=self.person, topic=self.topic)
       second_paragraph_chain = LLMChain(llm=self.llm, prompt=second_paragraph_prompt)
       return second_paragraph_chain
    
    def generate(self):
       opening_paragraph_chain = self.opening_paragraph_chain()
       second_paragraph_chain = self.second_paragraph_chain()
       """Chain together all of the paragraph chains"""
       overall_chain = SimpleSequentialChain(chains=[opening_paragraph_chain, second_paragraph_chain],
                                             verbose=True)
       return overall_chain.run()
