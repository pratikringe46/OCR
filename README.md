# OCR
OCR Hackathon project


# 🚀 OCR Hackathon Project - Setup Guide

This project is a Full-Stack OCR platform using **FastAPI** (Backend) and **Streamlit** (Frontend). It supports both **Printed** (Tesseract) and **Handwritten** (PaddleOCR) text extraction.

---

## **Phase 1: Prerequisites (Downloads)**
Before running the code, you must install these external tools on your machine.

### **1. Install Tesseract OCR**
* **Download:** [Click here for Windows Installer](https://github.com/UB-Mannheim/tesseract/wiki)
* **Action:** Run the `.exe` file.
* **IMPORTANT:** During installation, copy the "Destination Folder" path (usually `C:\Program Files\Tesseract-OCR`). You will need this for the code configuration.

### **2. Install Poppler (For PDF support)**
* **Download:** [Click here for Poppler Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
* **Action:** Extract the zip file to a safe location.
* **Setup:**
    1. Open the extracted folder and find the `bin` folder.
    2. Copy the full path to this `bin` folder.
    3. Add this path to your **System Environment Variables** under **Path**.

### **3. Install Python**
* Ensure you have Python 3.9 or higher installed.

---

## **Phase 2: Project Setup in VS Code**

1.  **Unzip the Project:** Extract the `OCR_Hackathon` folder to your Desktop.
2.  **Open in VS Code:** Right-click the folder and select **"Open with Code"**.
3.  **Open Terminal:** Press `Ctrl + ` ` (backtick) to open the terminal.

### **4. Create & Activate Virtual Environment**
Run the following commands in the VS Code terminal:

**Option A: Git Bash (Recommended)**
```bash
python -m venv venv
source venv/Scripts/activate

```
### Option B: Command Prompt / PowerShell
```cmd
python -m venv venv
.\venv\Scripts\activate
```

### **5. Install Dependencies**
Run this command to install all required libraries:

```Bash

pip install -r requirements.txt
```

## **Phase 3: Configuration (Critical Step)**
Open the file backend/ocr_engine.py in VS Code.

Look for the --- CONFIGURATION --- section near the top.

Verify the Tesseract Path:

```Python

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```
If you installed Tesseract in a different location (e.g., AppData), you must change this path to match your specific installation.

## **Phase 4: Running the App**
You need TWO separate terminals to run this app.

Terminal 1: Start Backend
Ensure (venv) is active.

Run:

```Bash
uvicorn backend.main:app --reload
```
Wait until you see "Application startup complete".

Terminal 2: Start Frontend
Click the + icon in the terminal panel to open a new terminal.

Activate the environment again:

For Git Bash:
```
source venv/Scripts/activate
```
For Windows Cmd:
```
.\venv\Scripts\activate
```

Run:

Bash
```
streamlit run frontend/app.py
```

A browser window will open automatically. You are ready to upload images!

