from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter


def summarize_start_to_finish(filename, openai_api_key):
    """Summarize a given text file with LangChain summarize chain functionality"""
    # Instantiate LLM
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    # Instantiate character-based text splitter
    text_splitter = CharacterTextSplitter()
    # Load text file
    with open(filename) as f:
        scraped_text = f.read()
    # Split text
    texts = text_splitter.split_text(scraped_text)
    # Generate a list of LangChain Documents out of the raw split text
    docs = [Document(page_content=t) for t in texts[:3]]
    # Generate a summary chain out of the docs, using the map_reduce method
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    # Generate the summary by running the chain against the list of LangChain Documents
    summary = chain.run(docs)
    return summary
