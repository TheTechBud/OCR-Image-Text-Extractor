import cv2
MIN_CONFIDENCE = 0.6

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
