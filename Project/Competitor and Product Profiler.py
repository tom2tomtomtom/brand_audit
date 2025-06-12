import requests
from bs4 import BeautifulSoup
import openai
from openai import OpenAI
import pandas as pd
import os
import json
import re

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# For backward compatibility
openai.api_key = os.getenv("OPENAI_API_KEY")

MAX_CONTENT_LENGTH = 12000

def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Failed to retrieve the page: {url} -- {e}")
        return None

def extract_links(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    links = soup.find_all('a', href=True)
    return [link['href'] for link in links if link['href'].startswith("http")]

def truncate_text(text, max_length=MAX_CONTENT_LENGTH):
    return text[:max_length] if len(text) > max_length else text

def extract_info_from_openai(text):
    text_to_send = truncate_text(text)

    messages = [
        {"role": "system", "content": "You are an AI that extracts structured data from webpage text."},
        {"role": "user", "content": (
            "Below is truncated HTML from a webpage. Identify:\n"
            "- CompanyName\n"
            "- SocialMediaURL\n"
            "- Products\n"
            "- ProductDescription\n\n"
            "Return your answer in valid JSON with exactly these keys:\n"
            "{\n"
            "  \"CompanyName\": \"...\",\n"
            "  \"SocialMediaURL\": \"...\",\n"
            "  \"Products\": \"...\",\n"
            "  \"ProductDescription\": \"...\"\n"
            "}\n\n"
            "Here is the webpage HTML:\n"
            f"{text_to_send}\n"
        )}
    ]

    try:
        # Use the new OpenAI client
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.5,
            max_tokens=500
        )
        
        assistant_content = response.choices[0].message.content.strip()
        cleaned_json = re.sub(r"```(json)?", "", assistant_content).strip()
        parsed_response = json.loads(cleaned_json)

        return {
            "CompanyName": parsed_response.get("CompanyName", ""),
            "SocialMediaURL": parsed_response.get("SocialMediaURL", ""),
            "Products": parsed_response.get("Products", ""),
            "ProductDescription": parsed_response.get("ProductDescription", "")
        }
    except Exception as e:
        print(f"Error with OpenAI API or JSON parsing: {e}")
        return None

def scrape_and_analyze(main_url):
    page_html = fetch_page(main_url)
    if not page_html:
        return

    subpage_links = extract_links(page_html)
    merged_data = {}

    for link in subpage_links:
        print(f"Analyzing subpage: {link}")
        subpage_html = fetch_page(link)
        if not subpage_html:
            continue

        parsed_json = extract_info_from_openai(subpage_html)
        if not parsed_json:
            continue

        company_name = parsed_json["CompanyName"].strip()
        if not company_name:
            continue

        if company_name not in merged_data:
            merged_data[company_name] = parsed_json
        else:
            existing = merged_data[company_name]
            if not existing["SocialMediaURL"] and parsed_json["SocialMediaURL"]:
                existing["SocialMediaURL"] = parsed_json["SocialMediaURL"]
            if not existing["Products"] and parsed_json["Products"]:
                existing["Products"] = parsed_json["Products"]
            if not existing["ProductDescription"] and parsed_json["ProductDescription"]:
                existing["ProductDescription"] = parsed_json["ProductDescription"]
            merged_data[company_name] = existing

    all_rows = [[val["CompanyName"], val["SocialMediaURL"], val["Products"], val["ProductDescription"]] for val in merged_data.values()]
    df = pd.DataFrame(all_rows, columns=["Company Name", "Social Media URL", "Product/s", "Product Description/Information"])
    df.to_csv("company_product_info.csv", index=False)
    print("Data saved to company_product_info.csv")

if __name__ == "__main__":
    main_url = "https://www.immuron.com.au/commercial-products/"
    scrape_and_analyze(main_url)
