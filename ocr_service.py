from PIL import Image
import numpy as np
import cv2
import cohere
from paddleocr import PaddleOCR
from config import COHERE_API_KEY, COHERE_MODEL
from cloudinary_service import download_image_from_url

# Initialize PaddleOCR
paddle_ocr = PaddleOCR()

# Initialize Cohere Client
if not COHERE_API_KEY:
    raise ValueError("Cohere API key not provided in config.py")
co = cohere.Client(COHERE_API_KEY)

def build_extraction_prompt(document_type, extracted_text):
    """
    Builds a structured prompt for Cohere LLM to extract key fields
    depending on the document type.
    """
    prompt = f"Extract the following information from the text: {extracted_text}\n\n"
    if document_type == "Salary Slip":
        prompt += "Find and return the values for: Net Salary, Gross Salary, Basic Salary.\n"
    elif document_type == "Profit and Loss Statement":
        prompt += "Find and return the values for: Total Revenue, Net Income.\n"
    elif document_type == "Check":
        prompt += "Find and return the values for: Account Number, Amount (in Rupees), Bank Name.\n"

    prompt += "Format each line strictly as 'Field: Value' (e.g. Net Salary: 50000). Do not include extra commentary, markdown, or bullet points."
    return prompt

def parse_llm_response(result_text, fallback_text=""):
    """
    Parses 'Field: Value' pairs from LLM text output into a clean dictionary.
    """
    data = {}
    for line in result_text.split("\n"):
        cleaned_line = line.strip().lstrip("-*• ").replace("**", "")
        if ":" in cleaned_line:
            key, value = cleaned_line.split(":", 1)
            key, value = key.strip(), value.strip()
            if key and value:
                data[key] = value

    if not data and fallback_text:
        data = {"Extracted Raw Text": fallback_text[:100]}
    return data

def process_single_image(image, document_type):
    """
    Takes a PIL Image, runs PaddleOCR, and uses Cohere to extract key fields.
    """
    # Convert PIL Image (RGB) to OpenCV format (BGR)
    image_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Perform OCR using PaddleOCR
    paddle_results = paddle_ocr.ocr(image_cv2)

    # Extract text from OCR results
    if not paddle_results or not paddle_results[0]:
        return {"Error": "No text detected in image"}

    texts = [line[1][0] for line in paddle_results[0] if line and len(line) > 1 and line[1]]
    extracted_text = " ".join(texts)

    if not extracted_text.strip():
        return {"Error": "No readable text extracted"}

    # Generate prompt for Cohere LLM
    prompt = build_extraction_prompt(document_type, extracted_text)

    # Query Cohere Chat API
    response = co.chat(model=COHERE_MODEL, message=prompt)
    result_text = response.text.strip()

    # Parse key-value results
    return parse_llm_response(result_text, fallback_text=extracted_text)

def process_documents(document_type, image_sources, is_url=False):
    """
    Process multiple document images (from either local filepaths or URLs).
    Returns a list of dictionaries with extracted information.
    """
    extracted_data = []
    for source in image_sources:
        try:
            if is_url:
                image = download_image_from_url(source)
                if image is None:
                    continue
            else:
                image = Image.open(source)

            data = process_single_image(image, document_type)
            extracted_data.append(data)

        except Exception as e:
            extracted_data.append({"Error": f"Failed to process image: {str(e)}"})

    return extracted_data
