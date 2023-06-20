import constants

from langchain import PromptTemplate, FewShotPromptTemplate 
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.llms import OpenAI
from dotenv import load_dotenv
from langchain.prompts.example_selector import LengthBasedExampleSelector
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import LLMChain, ConversationChain, SimpleSequentialChain, SequentialChain
from langchain.chains.summarize import load_summarize_chain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain import PromptTemplate
import json
from pathlib import Path
from pprint import pprint
from langchain.docstore.document import Document
from langchain.document_loaders import JSONLoader


from langchain.document_loaders import TextLoader


########### LOAD TEXT #############

# # Define the metadata extraction function.
# def metadata_func(record: dict, metadata: dict) -> dict:

#     metadata["sender_name"] = record.get("sender_name")
#     metadata["timestamp_ms"] = record.get("timestamp_ms")

#     return metadata


# loader = JSONLoader(
#     file_path='./example_data/facebook_chat.json',
#     jq_schema='.messages[]',
#     content_key="content",
#     metadata_func=metadata_func
# )

# data = loader.load()
def load_json(filepath, webpage_url):
    loader = JSONLoader(
        file_path=filepath,
        jq_schema="\"" + webpage_url + "\"")

    scraped_text = loader.load()
    return scraped_text

def load_text(filepath, webpage_url):
    # loader = TextLoader(filepath)

    scraped_text = json.loads(Path(filepath).read_text())
    # loader = UnstructuredFileLoader(filepath)
    # scraped_text = loader.load()
    scraped_text.get(webpage_url)
    pprint(scraped_text)
    # loader = PyPDFLoader("example_data/layout-parser-paper.pdf")
    # pages = loader.load_and_split()

    # Note - without a text splitter, it'll probably be too many tokens to handle.
    # print(f"Number of pages: {len(pages)}")
    # print(f"First document content: {pages[0]}")
    return scraped_text
    # with open(filepath) as f:
    #     scraped_text = f.read()
    #     return scraped_text

########### SPLITTING THE TEXT INTO CHUNKS #########
def split_text(scraped_text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )
    texts = text_splitter.split_text(scraped_text)

    # texts = text_splitter.create_documents(scraped_text)

    print(f"\nFirst chunk: {texts[0]}\n")
    print(f"Second chunk: {texts[1]}\n")

    return texts

########### CREATE DOCS #########
# Create Document objects for the texts (max 3 pages)
def create_docs(texts):
    docs = [Document(page_content=t) for t in texts[:3]]
    return docs

########### SUMMARIZE ################
def summarize(openai_api_key, docs):
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summarized_text = chain.run(docs)
    return summarized_text