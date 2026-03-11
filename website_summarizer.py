import requests
from bs4 import BeautifulSoup
from openai import OpenAI

from openai import OpenAI
client = OpenAI()

def get_website_text(url):
    """Download a website and return clean text and title"""
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # remove unnecessary tags
    for tag in soup(["script", "style", "img", "input"]):
        tag.decompose()

    title = soup.title.string if soup.title else "No title found"
    text = soup.get_text(separator="\n", strip=True)

    return title, text


def summarize_website(url):
    """Summarize a website using GPT"""
    
    title, text = get_website_text(url)

    prompt = f"""
    You are analyzing a website.

    Title: {title}

    Content:
    {text}

    Write a short markdown summary of the website.
    Ignore navigation or menu text.
    """

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# Example run
if __name__ == "__main__":
    url = input("Enter you url: ")
    summary = summarize_website(url)
    print(summary)