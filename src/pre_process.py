import cv2
#------Preprocessinng -----

def preprocess_image(image):
    if image is None:
        raise ValueError("Error: Image not found")

    #resize to make the image bigger
    image = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    #making it gray color
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(5, 5),0)          #BLurring techn.

    #Median filter to remove salt-pepper noise
    median = cv2.medianBlur(blur, 3)

    _, thresh = cv2.threshold(median,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    return image, morph