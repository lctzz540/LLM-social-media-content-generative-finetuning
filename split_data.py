import json
import os


def split_json_to_files(input_file, output_dir, n):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, "r") as f:
        data = json.load(f)

    num_items_per_file = len(data) // n

    chunks = [
        data[i: i + num_items_per_file]
        for i in range(0, len(data), num_items_per_file)
    ]

    for i, chunk in enumerate(chunks):
        output_file = os.path.join(output_dir, f"data_{i}.json")
        with open(output_file, "w") as f:
            json.dump(chunk, f, indent=4)


input_file = "./facebook/dataset_facebook-groups-scraper_2024-02-22_06-17-40-985.json"
output_dir = "./facebook/raw/"
n = 100

split_json_to_files(input_file, output_dir, n)
