<h1>🧠 OCR Text Extraction Tool</h1>

<h2>Overview</h2>

The OCR Text Extraction Tool is a web-based application that extracts textual content from images using Optical Character Recognition (OCR) techniques. The system integrates OpenCV for image preprocessing, an OCR engine for text detection, and Streamlit for the user interface.

The application demonstrates an end-to-end OCR pipeline, transforming raw images into structured and readable text through preprocessing, recognition, visualization, and post-processing.

This project highlights concepts in:  
💠Computer Vision  
💠Image preprocessing  
💠OCR pipelines  
💠Web-based ML applications  

## Key Features:  
💠Image upload through a web interface  
💠Image preprocessing to improve OCR accuracy  
💠Automatic text detection and extraction  
💠Bounding box visualization around detected text  
💠Text cleaning and formatting  
💠Modular and scalable project structure  

## System Architecture:  
    ┌─────────────────────────────────────────────────────────────────┐
    │                         USER INPUT                              │
    │                    (Image Upload via Web/CLI)                   │
    └────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                    IMAGE PREPROCESSING                          │
    │  ┌──────────┐    ┌──────────┐   ┌──────────┐   ┌──────────┐     │
    │  │ Resize   │ ──>│Grayscale │──>│  Blur    │──>│ Threshold│──>  │
    │  │  (3x)    │    │          │   │ Gaussian │   │   Otsu   │     │
    │  └──────────┘    └──────────┘   └──────────┘   └──────────┘     │
    │                                                                 │
    │  ┌──────────┐   ┌──────────┐                                    │
    │  │  Median  │──>│Morphology│                                    │
    │  │  Filter  │   │ Closing  │                                    │
    │  └──────────┘   └──────────┘                                    │
    └────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                      OCR ENGINE                                 │
    │                    (EasyOCR Reader)                             │
    │                                                                 │
    │  • Text Detection                                               │
    │  • Character Recognition                                        │
    │  • Bounding Box Extraction                                      │
    │  • Confidence Calculation                                       │
    └────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                   CONFIDENCE FILTERING                          │
    │              (Threshold: 0.6 / 60% default)                     │
    └────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                    VISUALIZATION                                │
    │         (Draw bounding boxes + confidence labels)               │
    └────────────────────────────┬────────────────────────────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                     TEXT CLEANING                               │
    │  • Remove OCR artifacts                                         │
    │  • Fix hyphenated words                                         │
    │  • Normalize spacing                                            │
    │  • Format paragraphs                                            │
    └────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                 OUTPUT GENERATION (Shown in app)                │
    │           ┌─────────────────────────────────┐                   │
    │           │   • extracted_text.txt          │                   │
    │           │   • results.csv                 │                   │
    │           │   • results.json                │                   │
    │           │   • result_image.png (boxed)    │                   │
    │           └─────────────────────────────────┘                   │
    └─────────────────────────────────────────────────────────────────┘
The system processes images through several layers to ensure improved text recognition accuracy.

## Project Structure
    OCR_project/
    ├──src
    │    ├── main.py                    # CLI application entry point
    │    ├── app.py                     # Streamlit web interface
    │    │
    │    ├── pre_process.py             # Image preprocessing pipeline
    │    ├── ocr_engine.py              # EasyOCR integration
    │    ├── visualisation.py           # Bounding box rendering
    │    ├── text_cleaner.py            # Post-processing utilities
    │    └── exports.py                 # Multi-format export functions
    │
    ├── images/                    # Sample Input image directory
    │   └── sample.png
    │
    ├── output/                    # Generated results
    │   ├── extracted_text.txt
    │   ├── results.csv
    │   ├── results.json
    │   └── result_image.png
    │
    ├── requirements.txt           # Python dependencies
    └── README.md                  # Project documentation

## 🔧 Module Breakdown
### 1. main.py - Command Line Interface
The standalone script for batch processing and automation.  

#### Workflow:  
1. Load image from images/sample.png  
2. Preprocess image  
3. Run OCR with confidence filtering  
4. Generate bounding box visualization  
5. Clean extracted text  
6. Export results (TXT, CSV, JSON, PNG)  

Key Configuration:

    python
    MIN_CONFIDENCE = 0.6        # Minimum confidence threshold
    OUTPUT_FOLDER = "output"    # Results directory
### 2. app.py - Web Application
Interactive Streamlit interface for real-time OCR.

#### Features:
💠 File uploader with format validation  
💠 Live preprocessing preview  
💠 Bounding box visualization  
💠 Cleaned text display  
💠 One-click download button  

#### Tech Stack:  
💠 Streamlit: Web framework  
💠 NumPy: Image array conversion  
💠 OpenCV: Image processing  

### 3. pre_process.py - Image Enhancement Pipeline
#### 5-Stage Preprocessing:


| Stage | Technique | Purpose |
|------|-----------|---------|
| Resize | 3× upscaling (INTER_CUBIC) | Improve text resolution |
| Grayscale | BGR → Grayscale conversion | Reduce image complexity |
| Gaussian Blur | 5×5 kernel | Remove Gaussian noise |
| Median Filter | 3×3 kernel | Remove salt-and-pepper noise |
| Otsu Thresholding | Adaptive binary threshold | Segment text from background |
| Morphology | 2×2 closing operation | Fill small gaps in text regions |

### Input:   ![alt text](images/1.jpg)
#
### Output: ![alt text](images/1.png) Enhanced binary image optimized for OCR
Extracted Text: ![alt text](images/image.png)

### 4. ocr_engine.py - Text Recognition
#### EasyOCR Configuration:

    reader = easyocr.Reader(['en'], gpu=False)

    results = reader.readtext(
        processed_image,
        paragraph=False,        # Word-level detection
        detail=1,               # Return coordinates + confidence
        contrast_ths=0.1,       # Low contrast threshold
        adjust_contrast=0.5     # Moderate contrast adjustment
    )
#### Output Format:

    [
        (bbox, text, confidence),
        ([(x1,y1), (x2,y2), (x3,y3), (x4,y4)], "Hello", 0.95),
        ...
    ]

### 5. visualisation.py - Bounding Box Renderer
#### Process:
1. Filter results by MIN_CONFIDENCE (default: 0.6)
2. Draw green rectangles around text regions
3. Add labels with text + confidence score
4. Return annotated image

#### OpenCV Functions Used:

💠 cv2.rectangle() - Draw bounding boxes  
💠 cv2.putText() - Add confidence labels

### 6. text_cleaner.py - Post-Processing
#### Cleaning Operations:

|Issue | Regex Pattern | Fix|
|------|--------------|------|
|Hyphenated words|	r'-\n' | Remove line break|
|OCR artifacts |	r'[~=_]' |Delete symbols|
|Multiple newlines |	r'\n+' |	Replace with space|
|Common errors |	Manual replacement	|"Iam" → "I am"|
|Space before punctuation |	r'\s([.,:;])'|	Remove space|
|Paragraph breaks |	r'([.!?])\s+'|	Add double newline|
#### Result: Clean, properly formatted text ready for downstream use.

### 7. exports.py - Multi-Format Export
#### Three Output Formats:

##### 1. TXT - Plain text extraction

    text
    Hello World (Confidence: 0.95)
    Welcome to OCR (Confidence: 0.89)
    CSV - Structured data

##### 2. text
    Text,Confidence
    Hello World,0.95
    Welcome to OCR,0.89
    JSON - API-ready format

##### 3. json
    [
    {"text": "Hello World", "confidence": 0.95},
    {"text": "Welcome to OCR", "confidence": 0.89}
    ]
## Features implemented:
💠 Image upload  
💠 Image preprocessing pipeline  
💠 OCR text detection  
💠 Bounding box visualization  
💠 Text cleaning  
💠 Modular code structure  
💠 Streamlit interface  

## Future Improvements
💠 PDF OCR support  
💠 Multi-Language Recognition  
💠 Deep Learning OCR models  
💠 Batch Image Processing  
💠 Document layout Detection  

#

Created By  
Soumabrata Das  
B.Tech CSE  
KIIT University
