# handler.py
import runpod, base64, tempfile, os
from paddleocr import PaddleOCR
from pdf2image import convert_from_path
import numpy as np

ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=True)

def handler(job):
    pdf_b64 = job["input"]["pdf_base64"]
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(base64.b64decode(pdf_b64))
        pdf_path = f.name
    
    images = convert_from_path(pdf_path, dpi=200)
    results = []
    for i, img in enumerate(images):
        result = ocr.ocr(np.array(img), cls=True)
        page_text = "\n".join([line[1][0] for block in result for line in block])
        results.append({"page": i + 1, "text": page_text})
    
    os.unlink(pdf_path)
    return {"pages": results}

runpod.serverless.start({"handler": handler})
