import os
import json


def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def save_json_file(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    folder_path = "./extracted/after_remove/"
    target_file_path = "./extracted/20-3.json"
    target_data = load_json_file(target_file_path)

    total_removed = 0

    for filename in os.listdir(folder_path):
        if filename.endswith(".json") and filename != target_file_path:
            file_path = os.path.join(folder_path, filename)
            data = load_json_file(file_path)
            removed_count = 0
            for item in data:
                if "text" in item:
                    text_to_check = item["text"]
                    for target_item in target_data:
                        if (
                            "text" in target_item
                            and target_item["text"] == text_to_check
                        ):
                            data.remove(item)
                            removed_count += 1
                            break
            total_removed += removed_count
            save_json_file(file_path, data)
            print(f"Deleted {removed_count} data from {filename}")

    print(f"Total deleted {total_removed} data")


if __name__ == "__main__":
    main()
