import easyocr
import cv2
import os
import csv
import json

#-------Configuration----
MIN_CONFIDENCE = 0.6
OUTPUT_FOLDER = "output"
#------Preprocessinng -----

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Error: Image not found")
    #resize to make the image bigger
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    #making it gray color
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5, 5),0)          #BLurring techn.
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return image, morph


def draw_boxes(image, results):
    for (bbox, text, prob) in results:
        if prob<MIN_CONFIDENCE:
            continue

        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))

        label = f"{text} ({round(prob, 2)})"

        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(image, label, top_left,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return image

def main():
    image_path = "images/sample.png"

    if not os.path.exists(image_path):
        print("Image not found in images folder!")
        return

    print("Preprocessing image...")
    try:
        original_image, processed_image = preprocess_image(image_path)
    except Exception as e:
        print(e)
        return
    #Using OCR as the main base
    print("Running OCR...")
    reader = easyocr.Reader(['en'], gpu=False)
    try:
        results = reader.readtext(processed_image, detail=1, paragraph=False)
    except Exception as e:
        print("OCR:Failed:  ",e)
        return
    extracted_text = ""
    ocr_data = [] #for JSN and CSV Files

    print("\nDetected Text")
    print("=" * 40)

    #Extracted text and normal printing of text
    for (bbox, text, prob) in results:
        if prob >= MIN_CONFIDENCE:
            print(f"Text: {text} | Confidence: {round(prob,2)}")
            extracted_text += f"{text} (Confidence: {round(prob,2)})\n"
            ocr_data.append({
            "text": text,
                "confidence": round(prob,2)
            })

    #Saving text file -----
    os.makedirs("output", exist_ok=True)
    with open("output/extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)
    
    #Saving CSV file-----
    csv_path = os.path.join(OUTPUT_FOLDER, "results.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Text", "Confidence"])
    for item in ocr_data:
        writer.writerow([item["text"], item["confidence"]])
    json_path = os.path.join(OUTPUT_FOLDER, "results.json")

    #Saving JSON file-----
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(ocr_data, f, indent=4)

    #bounding box image--------
    boxed_image = draw_boxes(original_image, results)
    cv2.imwrite("output/result_image.png", boxed_image)

    print("\nOCR Completed Successfully!")
    print("Saved Files in output folder.")


if __name__ == "__main__":
    main()



#   NEXT IS TO APPLY CUSTOM OCR MODEL AND ALSO AND CHANGE THE PREPROCESSING FILES & OCR MODEL