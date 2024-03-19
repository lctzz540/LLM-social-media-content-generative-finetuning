import json
import csv
import os


def read_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def read_csv(file_path):
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        return [row["text"] for row in reader]


def remove_entries(json_data, texts_to_remove):
    return [entry for entry in json_data if entry.get("text") not in texts_to_remove]


def export_json(data, file_path, encoding="utf-8"):
    with open(file_path, "w", encoding=encoding) as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def remove_entries_from_json(json_folder_path, csv_file_path, output_folder_path):
    json_files = [f for f in os.listdir(
        json_folder_path) if f.endswith(".json")]

    for json_file in json_files:
        json_file_path = os.path.join(json_folder_path, json_file)
        output_file_path = os.path.join(
            output_folder_path, f"after_remove_{json_file}")

        json_data = read_json(json_file_path)
        initial_count = len(json_data)
        texts_to_remove = read_csv(csv_file_path)
        updated_json_data = remove_entries(json_data, texts_to_remove)
        export_json(updated_json_data, output_file_path)
        removed_count = initial_count - len(updated_json_data)
        print(f"{removed_count} entries removed from {json_file}.")


json_folder_path = "./raw/"
csv_file_path = "./extracted/finished.csv"
output_folder_path = "./extracted/after_remove/"

remove_entries_from_json(json_folder_path, csv_file_path, output_folder_path)
