import easyocr

#Using OCR as the main base
def run_ocr(processed_image):

    print("Running OCR...")
    
    reader = easyocr.Reader(['en'], gpu=False)

    try:
        results = reader.readtext(processed_image,paragraph=False,detail=1,contrast_ths=0.1,adjust_contrast=0.5)
    except Exception as e:
        print("OCR:Failed:  ",e)
        return []

    return results