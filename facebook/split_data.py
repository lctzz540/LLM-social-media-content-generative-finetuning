import json
import os


def read_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def split_and_write(data, chunk_size, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    chunks = [data[i: i + chunk_size] for i in range(0, len(data), chunk_size)]

    for i, chunk in enumerate(chunks):
        output_file = os.path.join(output_directory, f"chunk_{i+1}.json")
        with open(output_file, "w") as file:
            json.dump(chunk, file, indent=4, ensure_ascii=False)


def split_json_files(file1, file2, chunk_size, output_directory):
    data1 = read_json(file1)
    data2 = read_json(file2)

    combined_data = data1 + data2

    split_and_write(combined_data, chunk_size, output_directory)


file1 = "./extracted/finished.json"
file2 = "./extracted/finished2.json"
chunk_size = 1000
output_directory = "./extracted/finished/"

split_json_files(file1, file2, chunk_size, output_directory)
