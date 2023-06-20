import openai

def getImage(key, topics):
    PROMPT = "The image should represent following values - " + topics + " and should be a cartoon"
    openai.api_key = key

    response = openai.Image.create(
        prompt=PROMPT,
        n=1,
        size="256x256", #can be changed to 512x512, 1024x1024
    )
    print(response["data"][0]["url"]);
    return response["data"][0]["url"]

#getImage("<open api key>", "asian, women, empowerment, beauty, pagent")