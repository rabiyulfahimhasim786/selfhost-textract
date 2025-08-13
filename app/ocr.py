from paddleocr import PaddleOCR
import cv2

ocr_model = PaddleOCR(use_angle_cls=True, lang='en')

def ocr_image(cv2_image):
    # input: cv2 image BGR
    # returns: list of dicts: {box, text, conf}
    res = ocr_model.ocr(cv2_image, cls=True)
    out = []
    for line in res:
        box = [[int(p[0]), int(p[1])] for p in line[0]]
        text, conf = line[1][0], float(line[1][1])
        out.append({'box': box, 'text': text, 'conf': conf})
    return out