import easyocr
import cv2
import os


def preprocess_image(image_path):
    image = cv2.imread(image_path)

    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image, gray


def draw_boxes(image, results):
    for (bbox, text, prob) in results:
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))

        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(image, text, top_left,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return image


def main():
    image_path = "images/sample.png"

    if not os.path.exists(image_path):
        print("Image not found in images folder!")
        return

    print("Preprocessing image...")
    original_image, processed_image = preprocess_image(image_path)

    cv2.imwrite("images/processed.png", processed_image)

    print("Running OCR...")
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext("images/processed.png", detail=1, paragraph=False)
    extracted_text = ""

    print("\nDetected Text")
    print("=" * 40)

    for (bbox, text, prob) in results:
        print(f"Text: {text} | Confidence: {round(prob, 2)}")
        extracted_text += f"{text} (Confidence: {round(prob, 2)})\n"

    # Save text file
    os.makedirs("output", exist_ok=True)
    with open("output/extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)

    # Save bounding box image
    boxed_image = draw_boxes(original_image, results)
    cv2.imwrite("output/result_image.png", boxed_image)

    print("\nOCR Completed Successfully!")
    print("Saved extracted_text.txt and result_image.png in output folder.")


if __name__ == "__main__":
    main()