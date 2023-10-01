import openai

def chatWithGPT(product_id, product_url, max_tokens=50):
    prompt = (
        f"Product ID: {product_id}\n"
        f"Product URL: {product_url}"
    )

    real_prompt = (
        f"{prompt}\n"
        "I have provided an outfit item information. I want you to return "
        "the clothing properties: name,short description, color and product ID. "
        "Then, suggest the occasion you think this clothing can be worn and vibes for these items using few words. "
        "Return your results in a single line for every item I provided."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides information about outfits."},
            {"role": "user", "content": real_prompt},
        ],
        max_tokens=max_tokens,  # Limit the response to a certain number of tokens
    )

    assistant_response = response.choices[0].message["content"]
    return assistant_response
