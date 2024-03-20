import json


def remove_duplicates(input_file, output_file):
    with open(input_file, "r") as f:
        data = json.load(f)

    unique_texts = set()
    unique_data = []
    for item in data:
        if item["text"] not in unique_texts:
            unique_texts.add(item["text"])
            unique_data.append(item)

    with open(output_file, "w") as f:
        json.dump(unique_data, f, indent=4, ensure_ascii=False)


input_file = "./extracted/20-3.json"
output_file = "./extracted/finished2.json"

remove_duplicates(input_file, output_file)
