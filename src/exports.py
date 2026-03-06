import os
import csv
import json

def save_results(extracted_text, ocr_data, OUTPUT_FOLDER):

    #Saving text file -----
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    with open(os.path.join(OUTPUT_FOLDER, "extracted_text.txt"), "w", encoding="utf-8") as f:
        f.write(extracted_text)

    #Saving CSV file-----
    csv_path = os.path.join(OUTPUT_FOLDER, "results.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Text", "Confidence"])

        for item in ocr_data:
            writer.writerow([item["text"], item["confidence"]])

    #Saving JSON file-----
    json_path = os.path.join(OUTPUT_FOLDER, "results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(ocr_data, f, indent=4)