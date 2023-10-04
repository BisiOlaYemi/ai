import os
import csv
import re

data_folder_path = os.path.join(os.path.dirname(__file__), 'Data')
output_path = os.path.join(data_folder_path, 'output.csv')

keywords_to_filter = ['kids', 'boy', 'baby', 'girls', 'romper']

processed_data = []
processed_product_ids = set()

def extract_and_process_details():
    try:
        with open(output_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Product Name', 'Description', 'Product ID', 'Product URL'])

            for file_name in os.listdir(data_folder_path):
                file_path = os.path.join(data_folder_path, file_name)

                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.read().split('\n')

                        for line in lines:
                            parts = line.split(';')

                            if len(parts) >= 11:
                                product_id = parts[8]

                                if product_id not in processed_product_ids:
                                    product_name = 'H&M;' + parts[5]
                                    product_description = ';'.join(parts[9:-6])
                                    urls = [url.strip() for url in parts[-6:-1]]

                                    unique_urls = list(set(urls))
                                    product_url = next((url for url in unique_urls if url.startswith('https://www2.hm.com')), '')

                                    should_filter = any(keyword in product_name.lower() for keyword in keywords_to_filter)

                                    if not should_filter:
                                        url_match = re.search(r'https://[^\s]+', product_description)
                                        product_url = url_match.group() if url_match else ''

                                        description = re.sub(r'https://[^\s]+', '', product_description).strip()

                                        csv_row = [product_name, description, product_id, product_url]
                                        csv_writer.writerow(csv_row)

                                        processed_data.append(csv_row)
                                        processed_product_ids.add(product_id)

        print('DataFile extraction to CSV completed.')

    except Exception as error:
        print('Error:', error)

extract_and_process_details()
