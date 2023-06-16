import constants
import response_body_generator
from scrape.scrape_chi_awe_org import ScrapeChiAWE

import os
import json

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

def scrape_all_websites():
    """
    Scrape all of the chi-AWE websites
    """
    scraped_text_dict = {}
    
    for website in constants.ALL_CHI_AWE_WEBSITES:
        scraper = ScrapeChiAWE(website)
        next_scrape = scraper.get_content()
        scraped_text_dict.update(next_scrape)
    
    filename = "website_text.txt"
    with open(constants.SCRAPED_TEXT_FILENAME,'w+') as f:
        f.write(str(scraped_text_dict))

if __name__ == '__main__':
    # scrape(constants.CHI_AWE_WEBSITE)
    scrape_all_websites()
