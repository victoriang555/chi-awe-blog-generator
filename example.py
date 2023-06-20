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

########## A FILE OF EXAMPLES FOR REFERENCE. THIS SCRIPT IS NOT USED IN THE ACTUAL APP ###########

template = "Tell me a {adjective} joke about {content}."

# Constructor
constructor_prompt = PromptTemplate(
    input_variables=["adjective", "content"],
    template=template,
)

# Output
print(f"Constructor: \
      {constructor_prompt.format(adjective='funny', content='chickens')}")


examples = [
    {"word": "happy", "antonym": "sad"},
    {"word": "tall", "antonym": "short"},
    {"word": "energetic", "antonym": "lethargic"},
    {"word": "sunny", "antonym": "gloomy"},
    {"word": "windy", "antonym": "calm"},
]

example_formatter_template = """Word: {word}
Antonym: {antonym}
"""

# Every example will be formatted using this prompt template
example_prompt = PromptTemplate(
    input_variables=["word", "antonym"],
    template=example_formatter_template,
)

# Optional example selector to narrow down the examples that will be used
example_selector = LengthBasedExampleSelector(
    examples=examples,
    example_prompt=example_prompt,
    max_length=25, # The num of words and newlines used by the formatter example section of the prompt
)

############ FEW SHOT LEARNING #########
# Note that you can only provide example_selector or examples as a field, not both at the same time
few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector, # optional field
    # examples=examples,
    example_prompt=example_prompt,
    prefix="Give the antonym of every input\n", # This gives the command
    suffix="Word: {input}\nAntonym: ", # Aims to guide the output of the LLM
    input_variables=["input"],
    example_separator="\n", # Used to separate the examples from the prefix and the suffix
)

# Generate a prompt
print(few_shot_prompt.format(input="big"))

############# OUTPUT PARSERS #############
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

parser = PydanticOutputParser(pydantic_object=Joke)
prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    },
)
# Ask the LLM to tell us a joke
joke_query = "Tell me a joke."
formatted_prompt = prompt.format_prompt(query=joke_query)

# # Send it to OpenAI
# load_dotenv() 
# # Note if you're going to use OpenAI, you'll need to supply your API key
# model = OpenAI(model_name='text-davinci-003', temperature=0.0)

# output = model(formatted_prompt.to_string())
# parsed_joke = parser.parse(output)
# print(parsed_joke)

########### LOAD TEXT #############
loader = PyPDFLoader("example_data/layout-parser-paper.pdf")
pages = loader.load_and_split()

# Note - without a text splitter, it'll probably be too many tokens to handle.
print(f"Number of pages: {len(pages)}")
print(f"First document content: {pages[0]}")

with open("example_data/state_of_the_union.txt") as f:
    state_of_the_union = f.read()

########### SPLITTING THE TEXT INTO CHUNKS #########
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

texts = text_splitter.create_documents(state_of_the_union)

print(f"\nFirst chunk: {texts[0]}\n")
print(f"Second chunk: {texts[1]}\n")

########### VECTORSTORES ##############
embeddings = OpenAIEmbeddings(Embed)
docsearch = Chroma.from_texts(texts, embeddings)

query = "What did the president say about Ketanji Brown Jackson"
docs = docsearch.similarity_search(query)

########### CHAINING #############
# Use chains to extract a model call to an LLM
load_dotenv()

llm = OpenAI(temperature=0.9)
prompt = PromptTemplate(
    input_variables=["company", "product"],
    template="What is a good name for {company} that makes {product}?",
)

chain = LLMChain(llm=llm, prompt=prompt)
print(chain.run({"company": "ABC Startup", "product": "colorful socks"}))

########## STATEFUL CHAINING USING MEMORY #######
load_dotenv()

chat = ChatOpenAI(temperature=0.9)
conversation = ConversationChain(
    llm=chat,
    memory=ConversationBufferMemory()
)

# Get it to respond partially to a question
out1 = conversation.run("Answer briefly. \
                        What are the first 3 colors of a rainbow?")
# To complete its answer
out2 = conversation.run("And the next 4?")

########## Chaining Chains #############
llm = OpenAI(temperature=0.9)
first_prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?"
)
chain_one = LLMChain(llm=llm, prompt=first_prompt)

second_prompt = PromptTemplate(
    input_variables=["company_name"],
    template="Write a catchphrase \
        for the following company: {company_name}",
)

chain_two = LLMChain(llm=llm, prompt=second_prompt)

overall_chain = SimpleSequentialChain(chains=[chain_one, chain_two],
                                      verbose=True)