import constants
import prepare_text

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
from langchain.chains import LLMChain, ConversationChain, SimpleSequentialChain, SequentialChain
from langchain.chains.summarize import load_summarize_chain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain import PromptTemplate

import streamlit as st

class ResponseBodyGenerator:
    def __init__(self, openai_api_key, person, topic, ask, secondary_ask, initiative, next_read, next_read_topics, alternative_read, alternative_read_topics):
        self.openai_api_key = openai_api_key
        self.person = person
        self.topic = topic
        self.ask = ask
        self.secondary_ask = secondary_ask
        self.initiative = initiative
        self.next_read = next_read
        self.next_read_topics = next_read_topics
        self.alternative_read = alternative_read
        self.alternative_read_topics = alternative_read_topics
        self.llm = OpenAI(model_name=constants.MODEL_NAME, openai_api_key=openai_api_key)
    
    def opening_paragraph_chain(self):
       """Generate the opening paragraph chain"""
       opening_paragraph_prompt = PromptTemplate(
            input_variables=[constants.PERSON, constants.TOPIC],
            template=constants.OPENING_PARAGRAPH_TEMPLATE
            )
       opening_paragraph_chain = LLMChain(llm=self.llm, prompt=opening_paragraph_prompt, output_key="synopsis")
       return opening_paragraph_chain

    def pitch_paragraph_chain(self):
       """Generate the paragraph making a pitch about supporting non-profits"""
       pitch_paragraph_prompt = PromptTemplate(
            input_variables=[constants.PERSON, constants.TOPIC],
            template=constants.PITCH_PARAGRAPH_TEMPLATE
            )
       pitch_paragraph_chain = LLMChain(llm=self.llm, prompt=pitch_paragraph_prompt, output_key="pitch")
       return pitch_paragraph_chain
    
    def ask_paragraph_chain(self):
       """Generate the paragraph asking them to do a specific thing for/with Chi-AWE"""
       ask_paragraph_prompt = PromptTemplate(
            input_variables=[constants.ASK, constants.INITIATIVE],
            template=constants.ASK_PARAGRAPH_TEMPLATE
            )
       ask_paragraph_chain = LLMChain(llm=self.llm, prompt=ask_paragraph_prompt, output_key="request")
       return ask_paragraph_chain
    
    def secondary_ask_paragraph_chain(self):
       """Generate the paragraph asking them to do something else for/with Chi-AWE if they couldn't do the first ask"""
       secondary_ask_paragraph_prompt = PromptTemplate(
            input_variables=[constants.ASK, constants.SECONDARY_ASK, constants.INITIATIVE],
            template=constants.ALTERNATIVE_ASK_PARAGRAPH_TEMPLATE
            )
       secondary_ask_paragraph_chain = LLMChain(llm=self.llm, prompt=secondary_ask_paragraph_prompt, output_key="secondary-request")
       return secondary_ask_paragraph_chain

    def next_read_paragraph_chain(self):
       """Generate a paragraph suggesting that they read another page on the website"""
       next_read_paragraph_prompt = PromptTemplate(
          input_variables = [constants.TOPIC, constants.NEXT_READ, constants.NEXT_READ_TOPICS],
          template=constants.NEXT_READ_PARAGRAPH_TEMPLATE
       )
       next_read_paragraph_chain = LLMChain(llm=self.llm, prompt=next_read_paragraph_prompt, output_key='next-suggested-reading')
       return next_read_paragraph_chain

    def alternative_read_paragraph_chain(self):
        """Generate a paragraph suggesting the reader read an alternative page on the website"""
        alternative_read_paragraph_prompt = PromptTemplate(
            input_variables = [constants.TOPIC, constants.ALTERNATIVE_READ, constants.ALTERNATIVE_READ_TOPICS],
            template=constants.ALTERNATIVE_READ_PARAGRAPH_TEMPLATE
        )
        alternative_read_paragraph_chain = LLMChain(llm=self.llm, prompt=alternative_read_paragraph_prompt, output_key='alternative-suggested-reading')
        return alternative_read_paragraph_chain

    def org_summary_paragraph_chain(self):
       """Generate the paragraph that summarizes what the org does"""
       scraped_text = prepare_text.load_text(constants.SCRAPED_JSON)
       texts = prepare_text.split_text(scraped_text=scraped_text)
       org_summary_paragraph_chain = prepare_text.docsearch(texts, self.openai_api_key)
       return org_summary_paragraph_chain
    
   #  def third_paragraph_chain(self):
   #     """Generate the paragraph that summarizes what the org does"""
   #     scraped_text = prepare_text.load_text(constants.SCRAPED_TEXT)
   #     texts = prepare_text.split_text(scraped_text=scraped_text)
   #     third_paragraph_chain = prepare_text.docsearch(texts, self.openai_api_key)
   #     return third_paragraph_chain
    
    def generate(self):
       # Generate paragraph chains
       opening_paragraph_chain = self.opening_paragraph_chain()
       pitch_paragraph_chain = self.pitch_paragraph_chain()
       ask_paragraph_chain = self.ask_paragraph_chain()
       secondary_ask_paragraph_chain = self.secondary_ask_paragraph_chain()
       next_read_paragraph_chain = self.next_read_paragraph_chain()
       alternative_read_paragraph_chain = self.alternative_read_paragraph_chain()
       org_summary_paragraph_chain= self.org_summary_paragraph_chain()
      #  third_paragraph_chain = self.third_paragraph_chain()

       #Chain together all of the paragraph chains
       overall_chain = SequentialChain(
          chains=[opening_paragraph_chain, pitch_paragraph_chain, ask_paragraph_chain, secondary_ask_paragraph_chain, next_read_paragraph_chain, alternative_read_paragraph_chain, org_summary_paragraph_chain],
          input_variables=[constants.PERSON, constants.TOPIC, constants.ASK, constants.SECONDARY_ASK, constants.INITIATIVE, constants.NEXT_READ, constants.NEXT_READ_TOPICS, constants.ALTERNATIVE_READ, constants.ALTERNATIVE_READ_TOPICS],
          output_variables=["synopsis", "pitch", "request", "secondary-request", "next-suggested-reading", "alternative-suggested-reading"],
          verbose=True)
       return overall_chain({"person": self.person, "topic": self.topic, "ask": self.ask, "secondary-ask": self.secondary_ask, "initiative": self.initiative, "next-read": self.next_read, "next-read-topics": self.next_read_topics, "alternative-read": self.alternative_read, "alternative-read-topics": self.alternative_read_topics})
