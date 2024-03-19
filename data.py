from dotenv import load_dotenv
import json
import os
import logging
import concurrent.futures
from openai import Client, RateLimitError

data_folder = "./facebook/extracted/after_remove/"

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def load_data(data_folder):
    data = []
    for filename in os.listdir(data_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(data_folder, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                data.extend(json.load(file))
    return data


def extract_information(client, text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant designed to output JSON, ensure that if the information is not provided, let give an empty string. Here is a real estate listing: ",
                },
                {
                    "role": "system",
                    "content": "\nType: Căn hộ, Mặt tiền, Văn phòng, Nhà ở, Đất, Unknown\nLocation: location\nArea: area\nNumber of floors: number_of_floors\nFrontage: frontage\nFurniture: furniture\nNumber of bedrooms: number_of_bedrooms\nNumber of bathrooms: number_of_bathrooms\nAmenities nearby: amenities_nearby\nPrice: price\nContact: contact\n",
                },
                {"role": "user", "content": text},
            ],
        )
        extracted = json.loads(response.choices[0].message.content)
        extracted["text"] = text
        return extracted
    except RateLimitError as e:
        logging.warning(f"Rate limit exceeded: {e}")
        return None


def process_texts(texts_batch, client):
    extracted = []
    unsuccessful = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [
            executor.submit(extract_information, client, text["text"])
            for text in texts_batch
        ]
        for future, text_data in zip(
            concurrent.futures.as_completed(futures), texts_batch
        ):
            result = future.result()
            if (
                result
                and result.get("Type", "")
                and result.get("Contact", "")
                and result.get("Location", "")
            ):
                extracted.append(result)
                logging.info(
                    f"Processed {len(extracted)} out of {
                        len(texts_batch)} texts."
                )
            else:
                unsuccessful.append(text_data["text"])

    return extracted, unsuccessful


def process_all_texts(texts_full, client):
    batch_size = 20
    total_texts = len(texts_full)
    processed_texts = 0
    extracted = []
    unsuccessful = []

    while texts_full:
        batch = texts_full[:batch_size]
        texts_full = texts_full[batch_size:]
        batch_extracted, batch_unsuccessful = process_texts(batch, client)
        extracted.extend(batch_extracted)
        unsuccessful.extend(batch_unsuccessful)
        processed_texts += len(batch_extracted)
        logging.info(f"Processed {processed_texts} out of {
                     total_texts} texts.")

    return extracted, unsuccessful


def remove_duplicates(data):
    unique_data = []
    unique_hashes = set()
    for item in data:
        item_tuple = tuple(sorted(item.items()))
        if item_tuple not in unique_hashes:
            unique_hashes.add(item_tuple)
            unique_data.append(item)
    return unique_data


def main():
    setup_logging()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = Client(api_key=OPENAI_API_KEY)
    data = load_data(data_folder)
    texts = [{"text": item.get("text", "")} for item in data]
    information_extracted, unsuccessful_processes = process_all_texts(
        texts, client)
    logging.info("Processed all texts.")
    logging.info(f"Data after processing: {len(information_extracted)}")
    unique_information_extracted = remove_duplicates(information_extracted)
    output_file_path = "./facebook/extracted/fbextracted_test.json"
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(
            unique_information_extracted, output_file, indent=4, ensure_ascii=False
        )
    logging.info("Data saved successfully.")


if __name__ == "__main__":
    main()
