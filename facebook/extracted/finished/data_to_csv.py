import os
import json
import csv

folder_path = "."

with open("data.csv", mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)

    writer.writerow(["query", "answer"])

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as json_file:
                data_list = json.load(json_file)
                for data in data_list:
                    query_parts = []
                    if "Type" in data:
                        query_parts.append(f"Group {data['Type']}")
                    if "Location" in data:
                        query_parts.append(f"Location {data['Location']}")
                    if "Area" in data:
                        query_parts.append(f"Area {data['Area']}")
                    if "Number of floors" in data:
                        query_parts.append(
                            f"Number of floors {data['Number of floors']}"
                        )
                    if "Frontage" in data:
                        query_parts.append(f"Frontage {data['Frontage']}")
                    if "Furniture" in data:
                        query_parts.append(f"Furniture {data['Furniture']}")
                    if "Number of bedrooms" in data:
                        query_parts.append(
                            f"Number of bedrooms {data['Number of bedrooms']}"
                        )
                    if "Number of bathrooms" in data:
                        query_parts.append(
                            f"Number of bathrooms {
                                data['Number of bathrooms']}"
                        )
                    if "Amenities nearby" in data:
                        query_parts.append(
                            f"Amenities nearby {data['Amenities nearby']}"
                        )
                    if "Price" in data:
                        query_parts.append(f"Price {data['Price']}")
                    if "Contact" in data:
                        query_parts.append(f"Contact {data['Contact']}")

                    query = ", ".join(query_parts)
                    writer.writerow([query, data["text"]])
