# chi-awe-blog-generator
A AI hackathon project to generate blog posts for the Chicago Asian Women Empowerment Non-profit (www.chi-awe.org)

# Setup
- This project will use python 3.11. 
- Please make sure to use the proper VM so that requirements handling will be smooth.
- Install requirements using the following command
```
make init
```

# Run the project on streamlit
- Streamlit is the host for the app. The repo is registered with the Streamlit Community Group. 
- The app is located here: https://victoriang555-chi-awe-blog-generator-streamlit-app-8chn4s.streamlit.app/
- You'll need an OpenAI API Key to pass it into the app.
- Note each query you make counts as tokens that are counted toward your OpenAI billing account.

# Run the project locally
Run the example project using the following command
```
make run-example
```

Run the scrape locally using the following command
```
make run
```

# LLM Terms to know
- Few Shot Learning - Give prompt a few examples to help guide its output. Great way to control the output of the LLM and guide its response.
- Output Parsers - Automatically parses the output of the language model into an object. More complicated, but very useful in structuring the outputs of the LLM
- Example Selectors - Choose which examples to put in the prompt. Goal could be to optimize for cost-savings, relevance, etc.
- Chat Prompt Template - 
