from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import os
import json

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/extract-text/")
async def extract_text_from_invoice(file: UploadFile = File(...)):
    # Save uploaded image file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Open image and extract text using Tesseract
    image = Image.open(file_path)
    raw_text = pytesseract.image_to_string(image)

    # Build JSON response data
    result_data = {"extracted_text": raw_text}

    # Save to pretty JSON file
    base_name = os.path.splitext(file.filename)[0]
    json_path = os.path.join(OUTPUT_DIR, f"{base_name}.json")
    with open(json_path, "w") as json_file:
        json.dump(result_data, json_file, indent=4)

    # Do NOT delete the uploaded file (keep it in uploads)
    # os.remove(file_path)

    # Return the result as JSON
    return JSONResponse(content=result_data)
