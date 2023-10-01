import os
import openai
import csv

openai.api_key = "" # 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

data_folder_path = os.path.join(os.path.dirname(__file__), 'Data')
output_path = os.path.join(data_folder_path, 'output.csv')
output_recommendations_path = os.path.join(data_folder_path, 'recommendations.csv')

keywords_to_filter = ['kids', 'boy', 'baby', 'girls', 'romper']

def chatWithGPT(product_id, product_url):
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
    return assistant_response

def process_and_recommend_clothing():
    try:
        recommendations_data = []

        with open(output_path, 'r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  

            for row in csv_reader:
                product_name, description, product_id, product_url = row

                recommendations_data_per_product = []  

                response_count = 0
                while response_count < 5:
                    recommendation = chatWithGPT(product_id, product_url)
                    recommendations_data_per_product.append(recommendation)
                    response_count += 1

                recommendations_data.append({
                    "Product Name": product_name,
                    "Description": description,
                    "Product ID": product_id,
                    "Product URL": product_url,
                    "Recommendations": "\n".join(recommendations_data_per_product)
                })

                if response_count >= 5:
                    break

        with open(output_recommendations_path, 'w', newline='', encoding='utf-8') as recommendations_file:
            fieldnames = ["Product Name", "Description", "Product ID", "Product URL", "Recommendations"]
            writer = csv.DictWriter(recommendations_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(recommendations_data)

        print('Recommendation completed.')

    except Exception as error:
        print('Error:', error)

process_and_recommend_clothing()
