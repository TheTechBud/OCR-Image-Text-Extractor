import re

def clean_ocr_text(text):

    # Fix hyphenated words (comfort- able → comfortable)
    text = re.sub(r'-\n', '', text)

    # Remove random OCR characters
    text = re.sub(r'[~|=_]', '', text)

    # Replace multiple line breaks with single space
    text = re.sub(r'\n+', ' ', text)

    # Fix common OCR word issues
    text = text.replace("Iam", "I am")

    # Fix spaces before punctuation
    text = re.sub(r'\s([.,:;])', r'\1', text)

    # Create paragraph breaks after sentences
    text = re.sub(r'([.!?])\s+', r'\1\n\n', text)

    return text.strip()