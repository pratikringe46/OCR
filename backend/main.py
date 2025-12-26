from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid
from backend.ocr_engine import run_ocr
# Note: In VS Code, sometimes imports need to be 'from ocr_engine' if running directly inside backend folder.
# But usually 'from backend.ocr_engine' is correct if running from root.

app = FastAPI()

# Create temp folder if it doesn't exist
TEMP_FOLDER = "temp"
os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "OCR API is running"}

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...), mode: str = Form(...)):
    """
    Receives an image and a mode (printed/handwritten).
    Returns the extracted text.
    """
    try:
        # 1. Generate unique filename to avoid conflicts
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(TEMP_FOLDER, unique_filename)

        # 2. Save the uploaded file locally
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 3. Run OCR
        extracted_text = run_ocr(file_path, mode)

        # 4. Cleanup (Optional: delete file after processing to save space)
        # os.remove(file_path)

        return {
            "filename": file.filename,
            "mode": mode,
            "text": extracted_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))