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
            model="gpt-3.5-turbo-0125",
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
        try:
            extracted = json.loads(response.choices[0].message.content)
        except:
            return None
        extracted["text"] = text
        return extracted
    except:
        return None


def process_texts(texts_batch, client):
    extracted = []
    unsuccessful = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
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


def main():
    setup_logging()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = Client(api_key=OPENAI_API_KEY)
    data = load_data(data_folder)
    texts = [{"text": item.get("text", "")} for item in data]
    batch_size = 50

    processed_texts = 0

    total_texts = len(texts)

    output_file_path = "./facebook/extracted/20-3.json"

    with open(output_file_path, "a", encoding="utf-8") as output_file:
        while texts:
            batch = texts[:batch_size]
            texts = texts[batch_size:]
            information_extracted, unsuccessful_processes = process_texts(
                batch, client)
            for item in information_extracted:
                json.dump(item, output_file, ensure_ascii=False)
                output_file.write('\n')
            processed_texts += len(batch)
            logging.info(f"Processed {processed_texts} out of {
                         total_texts} texts.")

    logging.info("Processed all texts.")
    logging.info(f"Data saved successfully.")


if __name__ == "__main__":
    main()
