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

from langchain.document_loaders import TextLoader


########### LOAD TEXT #############

# Define the metadata extraction function.
def metadata_func(record: dict, metadata: dict) -> dict:

    metadata["sender_name"] = record.get("sender_name")
    metadata["timestamp_ms"] = record.get("timestamp_ms")

    return metadata


loader = JSONLoader(
    file_path='./example_data/facebook_chat.json',
    jq_schema='.messages[]',
    content_key="content",
    metadata_func=metadata_func
)

data = loader.load()

def load_text(filepath):
    # loader = TextLoader(filepath)

    scraped_text = json.loads(Path(filepath).read_text())
    # loader = UnstructuredFileLoader(filepath)
    # scraped_text = loader.load()
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

    texts = text_splitter.create_documents(scraped_text)

    print(f"\nFirst chunk: {texts[0]}\n")
    print(f"Second chunk: {texts[1]}\n")

    return texts

########### VECTORSTORES ##############
def docsearch(texts, openai_api_key):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    docsearch = Chroma.from_texts(texts, embeddings)

    query = constants.WEBSITE_SUMMARY_QUERY
    docs = docsearch.similarity_search(query)
    return docs

########### SUMMARIZE ################
def summarize(docs):
    llm = OpenAI(temperature=0)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    # summarized_text = chain.run(docs)
    return chain