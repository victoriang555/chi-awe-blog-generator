# chi-awe-blog-generator
A AI hackathon project to generate blog posts for the Chicago Asian Women Empowerment Non-profit (www.chi-awe.org)

# User Instructions
## Setup
1. Generate your own OpenAI API key if you don't have one already. You are provided $5 free credits when you open a new account with an actual (not virtual) phone number, and it should be plenty of credit to run this service. See https://platform.openai.com/account/api-keys 
2. Navigate to this website where the app is hosted: https://victoriang555-chi-awe-blog-generator-main-cntmyp.streamlit.app/
3. Copy your API key into the field in the left nav
4. Enter all of the requested fields.

## Use case 1: Scrape all Chi-AWE Websites for content
If the Chi-AWE websites have been updated since the last time you used this app, you should scrape again. This will ensure that the app is using the most up-to-date content. The app will respond with the content is scraped in a json format, with the keys being the specific page's url and the value being the text it was able to scrape. You can use this content as guidance for determining how SEO-friendly each of your pages are and see what content you might be missing! Also consider how many times a particular search term shows up in the scraped content- if you want that search term to be more relevant to search engines, identify the webpages that are missing that search term and add it! 

To scrape all Chi-AWE websites, you actually don't need an OpenAI API key! All you need to do is click "Scrape".

## Use Case 2: Generate an Image
Images can make webpages look more dynamic and user friendly. They can be used anywhere on your website, including the blog post! This app will help you generate an image based on the input topics you've provided and the Chi-AWE initiative/program that you've referenced. 

To generate an image:
1. You will need to input your OpenAI API Key
2. You'll also need to fill out the following fields - Topic and Initiative
3. Then press the "Generate Image" button
4. The app will respond with a link to an image. Open the link in a new tab and right click and choose your save options. If you don't like the generated image, you can generate another one by pressing the button again. You can also change the topic and initiative and re-press the button to see if any better outputs come!

## Use Case 3: Generate Paragraphs for a Blog Post
If you want to generate paragraphs for a blog post, follow the instructions below. The app will generate multiple pages that first give an overview of the topic you've chosen, a pitch for why they should support the initiative you've chosen, a specific ask of the reader you've supplied, a secondary ask of the reader, a paragraph explaining another webpage you suggest they read, and a final paragraph explaining an additional webpage to read.  

To generate blog post paragraphs:
1. You will need to input your OpenAI API Key
2. You'll also need to fill out the following fields: Target Blog Post Reader Demographics, Blog Post Topic, Primary Reader Ask, Initiative, Secondary Reader Ask, Next Suggested Reading, Next Suggested Reading Keywords, Alternative Suggested Reading, Alternative Reading Keywords
3. Click the "Request Blog" button
4. The response will give you the paragraphs that you can edit, copy, and paste into your website editor! 

## Use Case 4: [In Beta] Generate an Org Summary from a Particular Webpage's Text
Note, this is in beta, meaning that it might not work as expected when you're trying it out, depending on how far along in our development of it we're at. 

The intended behavior is you would be able to generate an org summary paragraph based on the text from a particular page on the website. For example, if there is a "mission and vision" page that also includes history of the org, you could supply the url to that page and the app will scrape that particular page's text and then generate a Chi-AWE summary from that text supported with any OpenAI-generated text.

To generate an org summary:
1. You will need to input your OpenAI API Key
2. You will need to fill out the following fields - Webpage to Scrape, 

## Future Potential Use Case
This can potentially be integrated into the Chi-AWE website, and, if given the website visitor's demographics and user history through the cookies, the app could generate a customized pitch to the visitor recommending a particular initiative to learn more about or a particular action-item for them to get involved (if they've already visited the websites multiple times). This can be in the form of a pop-up on the landing page of any or all of the Chi-AWE websites.

# Developer Setup
- This project will use python 3.11. 
- Please make sure to use the proper VM so that requirements handling will be smooth.
- Install requirements using the following command
```
make init
```

## Run the project on streamlit
- Streamlit is the host for the app. The repo is registered with the Streamlit Community Group. 
- The app is located here: https://victoriang555-chi-awe-blog-generator-main-cntmyp.streamlit.app/
- You'll need an OpenAI API Key to pass it into the app.
- Note each query you make counts as tokens that are counted toward your OpenAI billing account.

## Run the project locally
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

# More Resources
- Example concept tutorial for chaining https://towardsdatascience.com/a-gentle-intro-to-chaining-llms-agents-and-utils-via-langchain-16cd385fca81