import os
import openai
import csv

openai.api_key = ""  # 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

data_folder_path = os.path.join(os.path.dirname(__file__), 'Data')
output_path = os.path.join(data_folder_path, 'output.csv')
output_recommendations_path = os.path.join(data_folder_path, 'recommendations.csv')

keywords_to_filter = ['kids', 'boy', 'baby', 'girls', 'romper']

def chatWithGPT(product_ids, product_urls):
    recommendations = []

    for product_id, product_url in zip(product_ids, product_urls):
        real_prompt = (
            f"Product ID: {product_id}\n"
            f"Product URL: {product_url}\n\n"
            "I have provided an outfit item information. I want you to return "
            "the clothing properties: name, short description, color, and product ID. "
            "Then, suggest the occasion you think this clothing can be worn and vibes for these items using few words. "
            "Return your results in a single line for every item I provided."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides information about outfits."},
                {"role": "user", "content": real_prompt},
            ],
        )

        assistant_response = response.choices[0].message["content"]
        recommendations.append({"Product ID": product_id, "Recommendation": assistant_response})

    return recommendations

def process_and_recommend_clothing():
    try:
        recommendations_data = []

        with open(output_path, 'r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  

            product_ids = []
            product_urls = []

            for row in csv_reader:
                product_name, description, product_id, product_url = row
                product_ids.append(product_id)
                product_urls.append(product_url)

            for product_id, recommendation in chatWithGPT(product_ids, product_urls):
                recommendations_data.append({
                    "Product ID": product_id,
                    "Recommendation": recommendation
                })

        with open(output_recommendations_path, 'w', newline='', encoding='utf-8') as recommendations_file:
            fieldnames = ["Product ID", "Recommendation"]
            writer = csv.DictWriter(recommendations_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(recommendations_data)

        print('Recommendation completed.')

    except Exception as error:
        print('Error:', error)

process_and_recommend_clothing()
