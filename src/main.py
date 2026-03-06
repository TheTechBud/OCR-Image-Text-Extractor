import cv2
import os
import re
from pre_process import preprocess_image
from visualisation import draw_boxes
from ocr_engine import run_ocr
from exports import save_results
from text_cleaner import clean_ocr_text

#-------Configuration----
MIN_CONFIDENCE = 0.6
OUTPUT_FOLDER = "output"

def main():
    image_path = "images/sample.png"

    if not os.path.exists(image_path):
        print("Image not found in images folder!")
        return
    
    extracted_text = ""
    ocr_data = []
    
    print("Preprocessing image...")
    try:
        original_image, processed_image = preprocess_image(image_path)
    except Exception as e:
        print(e)
        return
    
    results = run_ocr(processed_image)      #running ocr and savin it 
    if not results:
        print("No text detected.")


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
    extracted_text = clean_ocr_text(extracted_text)
    save_results(extracted_text, ocr_data, OUTPUT_FOLDER)

    #bounding box image--------
    boxed_image = draw_boxes(original_image, results)
    cv2.imwrite("output/result_image.png", boxed_image)

    print("\nOCR Completed Successfully!")
    print("Saved Files in output folder.")


if __name__ == "__main__":
    main()



#   NEXT IS TO APPLY CUSTOM OCR MODEL AND ALSO AND CHANGE THE PREPROCESSING FILES & OCR MODEL