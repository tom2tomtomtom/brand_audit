import openai
import pandas as pd

def extract_main_takeaways(article_text):
    """
    Makes a GPT call to extract 3 main takeaways from the article text.
    Returns a string containing those takeaways.
    """
    messages = [
        {
            "role": "system",
            "content": "You are an AI that extracts the 3 main takeaways from a text about gut health products, and writed them in a way that is easy to understand for non-technical readers."
        },
        {
            "role": "user",
            "content": (
                f"Article text:\n{article_text}\n\n"
                "Please list the 3 main takeaways from this article."
            )
        }
    ]

    response = openai.chat.completions.create(
        model="gpt-4o-mini", 
        messages=messages,
        temperature=0,
        max_tokens=100
    )

    takeaways = response.choices[0].message.content.strip()
    return takeaways

def main():
    df = pd.read_excel("Dataset with news articles.xlsx")
    relevant_articles = []

    for idx, row in df.iterrows():
        article_text = row["Description"]
        
        # First: classify whether the article is about a gut health product
        messages = [
            {"role": "system", "content": "You are an AI that classifies whether articles are about gut health products."},
            {
                "role": "user",
                "content": (
                    f"Title: {row['Title']}\n"
                    f"URL: {row['URL']}\n"
                    f"Date: {row['Date']}\n"
                    f"Description:\n{article_text}\n\n"
                    "Question: Is this article about a gut health product?\n"
                    "Reply 'Yes' or 'No' only."
                )
            }
        ]

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0,
            max_tokens=3
        )

        reply = response.choices[0].message.content.strip()

        if reply.lower().startswith("yes"):
            row_copy = row.copy()  # Copy the row so we can safely add a new column
            row_copy["Main Takeaways"] = extract_main_takeaways(article_text)

            relevant_articles.append(row_copy)

    df_relevant = pd.DataFrame(relevant_articles)
    df_relevant.to_excel("filtered_articles_extra.xlsx", index=False)
    print("Done! Filtered articles with main takeaways saved to 'filtered_articles.xlsx'.")

if __name__ == "__main__":
    main()
