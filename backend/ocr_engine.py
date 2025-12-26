import cv2
import numpy as np
import pytesseract
from paddleocr import PaddleOCR
import os

# --- CONFIGURATION ---
# IMPORTANT: If you are on Windows and Tesseract is not in your PATH, uncomment the line below:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\prati\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Initialize PaddleOCR (Loads model into memory once. NOTE: First run will download ~20MB model)
paddle_engine = PaddleOCR(use_angle_cls=True, lang='en')

def preprocess_image(image_path):
    """
    Cleans the image for better OCR accuracy:
    1. Grayscale
    2. Gaussian Blur (removes noise)
    3. Adaptive Thresholding (makes text pop against background)
    """
    img = cv2.imread(image_path)
    
    # Check if image loaded
    if img is None:
        raise ValueError("Image not found or invalid format.")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Binarization (Black text on white background)
    processed_img = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    return processed_img

def extract_text_tesseract(image_path):
    """Best for Standard Printed Documents"""
    processed_img = preprocess_image(image_path)
    # config: --psm 3 (Auto page segmentation)
    text = pytesseract.image_to_string(processed_img, config='--psm 3')
    return text

# def extract_text_paddle(image_path):
#     """Best for Handwritten or Messy Text"""
#     # PaddleOCR handles preprocessing internally better for wild text
#     result = paddle_engine.ocr(image_path)
    
#     full_text = ""
#     # Parse Paddle's complex output format
#     if result and result[0]:
#         for line in result[0]:
#             text_segment = line[1][0]
#             full_text += text_segment + "\n"
            
#     return full_text


# def extract_text_paddle(image_path):
#     # """Best for Handwritten or Messy Text"""
    
#     # 1. READ IMAGE
#     img = cv2.imread(image_path)
    
#     # 2. IMAGE THICKENING (The "Ink Thickener")
#     # Handwriting is often thin/faint. We dilate it to make strokes connected.
#     # This stops "H e l l o" from being read as 5 separate boxes.
#     kernel = np.ones((2, 2), np.uint8)
#     img = cv2.dilate(img, kernel, iterations=1)
    
#     # Save a temp file for Paddle to read (Paddle needs a file path or numpy array)
#     # We pass the numpy array 'img' directly to avoid disk I/O
#     result = paddle_engine.ocr(img)

#     full_text = ""
    
#     # if result and result[0]:
#     #     # Paddle returns: [[[box_coords], [text, confidence]], ...]
#     #     boxes = result[0]
        
#     #     # Sort boxes by vertical position (top to bottom)
#     #     # box[0][0][1] is the Y-coordinate of the top-left corner
#     #     boxes.sort(key=lambda x: x[0][0][1])
        
#     #     # LOGIC: Group words into lines
#     #     current_line_y = -100 # Start with a dummy value
#     #     line_threshold = 20   # Pixels. If words are within 20px vertically, they are one line.
        
#     #     for box in boxes:
#     #         box_coords = box[0]
#     #         text_segment = box[1][0]
#     #         y_pos = box_coords[0][1] # Y-coord of top left
            
#     #         # Check if this word belongs to the current line
#     #         if abs(y_pos - current_line_y) < line_threshold:
#     #             full_text += " " + text_segment # Add space, same line
#     #         else:
#     #             # New line detected
#     #             if current_line_y != -100: # Don't add newline at the very start
#     #                 full_text += "\n"
#     #             full_text += text_segment
#     #             current_line_y = y_pos

#     if result and result[0]:
#         # CRITICAL FIX: Convert Paddle's custom object to a standard Python list
#         boxes = list(result[0])
        
#         # Now we can sort it safely
#         # Sort boxes by vertical position (top to bottom)
#         boxes.sort(key=lambda x: x[0][0][1])
        
#         # LOGIC: Group words into lines
#         current_line_y = -100 
#         line_threshold = 20   
        
#         for box in boxes:
#             box_coords = box[0]
#             text_segment = box[1][0]
#             y_pos = box_coords[0][1] 
            
#             if abs(y_pos - current_line_y) < line_threshold:
#                 full_text += " " + text_segment 
#             else:
#                 if current_line_y != -100: 
#                     full_text += "\n"
#                 full_text += text_segment
#                 current_line_y = y_pos

#     return full_text



# def extract_text_paddle(image_path):
#     """Best for Handwritten or Messy Text (Robust Version)"""
    
#     # 1. READ IMAGE
#     img = cv2.imread(image_path)
#     if img is None:
#         return "Error: Could not read image file."
    
#     # 2. THICKEN INK (Helps connect broken letters)
#     kernel = np.ones((2, 2), np.uint8)
#     img = cv2.dilate(img, kernel, iterations=1)
    
#     # 3. RUN OCR
#     # We add a try-except block here in case Paddle itself fails internally
#     try:
#         result = paddle_engine.ocr(img)
#     except Exception as e:
#         print(f"PaddleOCR internal error: {e}")
#         return ""

#     full_text = ""
    
#     # 4. PARSE RESULTS SAFELY
#     if result and result[0]:
#         # Convert to list to enable sorting
#         boxes = list(result[0])
        
#         # Sort by Top-to-Bottom (Y-coordinate)
#         # We use a safe key function that won't crash if a box is malformed
#         def safe_sort_key(box):
#             try:
#                 # box[0] = coords, box[0][0] = top-left point, box[0][0][1] = y
#                 return box[0][0][1]
#             except:
#                 return 0 # Default to top if data is bad

#         boxes.sort(key=safe_sort_key)
        
#         current_line_y = -100
#         line_threshold = 20
        
#         for box in boxes:
#             try:
#                 # --- SAFETY CHECK BLOCK ---
#                 # Ensure box has the expected structure: [coords, (text, conf)]
#                 if not box or len(box) < 2:
#                     continue
                
#                 text_info = box[1] # This should be ("text", confidence)
#                 if not text_info or len(text_info) < 1:
#                     continue
                
#                 text_segment = text_info[0] # The actual text string
                
#                 # Skip empty strings
#                 if not text_segment:
#                     continue
#                 # ---------------------------

#                 box_coords = box[0]
#                 y_pos = box_coords[0][1]
                
#                 # Logic: Group words into lines
#                 if abs(y_pos - current_line_y) < line_threshold:
#                     full_text += " " + text_segment
#                 else:
#                     if current_line_y != -100:
#                         full_text += "\n"
#                     full_text += text_segment
#                     current_line_y = y_pos
                    
#             except Exception as e:
#                 # If one specific word fails, print error to terminal but KEEP GOING
#                 print(f"Skipped a bad text box: {e}")
#                 continue

#     return full_text



def extract_text_paddle(image_path):
    """Best for Handwritten or Messy Text (Fixed Version)"""
    
    # 1. READ IMAGE
    img = cv2.imread(image_path)
    if img is None:
        return "Error: Could not read image file."

    # REMOVED: The cv2.dilate lines were erasing the text.
    
    # 2. RUN OCR
    try:
        # result structure: [[[[box], [text, conf]], ...]]
        result = paddle_engine.ocr(img)
    except Exception as e:
        print(f"PaddleOCR internal error: {e}")
        return ""

    # DEBUG: Print to terminal to see if Paddle found anything at all
    print(f"DEBUG: Raw Paddle Result: {result}") 

    full_text = ""
    
    # 3. PARSE RESULTS
    if result and result[0]:
        # Convert to list for sorting
        boxes = list(result[0])
        
        # Sort Top-to-Bottom
        def safe_sort_key(box):
            try:
                return box[0][0][1]
            except:
                return 0
        boxes.sort(key=safe_sort_key)
        
        current_line_y = -100
        line_threshold = 20 
        
        for box in boxes:
            try:
                # Structure Check
                if not box or len(box) < 2:
                    continue
                
                text_info = box[1] # ("text", confidence)
                if not text_info or len(text_info) < 1:
                    continue
                
                text_segment = text_info[0]
                
                # Logic: Group words into lines
                box_coords = box[0]
                y_pos = box_coords[0][1]
                
                if abs(y_pos - current_line_y) < line_threshold:
                    full_text += " " + text_segment
                else:
                    if current_line_y != -100:
                        full_text += "\n"
                    full_text += text_segment
                    current_line_y = y_pos
                    
            except Exception as e:
                continue

    # If full_text is still empty after loop, check why
    if not full_text:
        return "No text detected. Try a clearer image."

    return full_text

def run_ocr(image_path, mode="printed"):
    if mode == "handwritten":
        return extract_text_paddle(image_path)
    else:
        return extract_text_tesseract(image_path)