import os
import cv2
import tempfile
import json
from app.ocr import ocr_image
from app.layout import detect_layout
from pdf2image import convert_from_path
import pdfplumber
import re

GSTIN_REGEX = r"[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}"


def pdf_to_images(pdf_path, dpi=300):
    pages = convert_from_path(pdf_path, dpi=dpi)
    return [cv2.cvtColor(np.array(p), cv2.COLOR_RGB2BGR) for p in pages]


def image_from_file(path):
    img = cv2.imread(path)
    if img is None:
        # maybe it's a PDF
        pages = convert_from_path(path, dpi=300)
        return [cv2.cvtColor(np.array(p), cv2.COLOR_RGB2BGR) for p in pages]
    return [img]


def find_gstin_in_text(text):
    match = re.search(GSTIN_REGEX, text.replace(' ', '').upper())
    return match.group(0) if match else None


def process_file(path):
    # returns JSON with pages -> ocr + layout + simple kv extraction
    is_pdf = path.lower().endswith('.pdf')
    if is_pdf:
        pages = convert_from_path(path, dpi=300)
        pages = [cv2.cvtColor(np.array(p), cv2.COLOR_RGB2BGR) for p in pages]
    else:
        pages = [cv2.imread(path)]

    out = {'file': os.path.basename(path), 'pages': []}
    for i, img in enumerate(pages):
        ocr = ocr_image(img)
        layout = detect_layout(img)

        # naive KV: join all ocr text and search for GSTIN
        joined = ' '.join([w['text'] for w in ocr])
        gstin = find_gstin_in_text(joined)

        out['pages'].append({
            'page': i+1,
            'gstin_candidate': gstin,
            'ocr': ocr,
            'layout_blocks': [{ 'type': b.type, 'bbox': b.coordinates } for b in layout]
        })

    # write to /tmp as a record (for demo)
    with open(f'/tmp/extract_{os.path.basename(path)}.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    return out