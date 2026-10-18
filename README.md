# 📄 Document OCR, Analysis, and Visualization

An interactive application that performs OCR on financial documents (Salary Slips, Profit & Loss Statements, Bank Checks), uses Cohere LLM to extract key fields, and visualizes the results with charts and summary tables.

---

## 🗂️ Project Structure

The project has been split into small, modular files to make each component simple to understand, modify, and test:

| File | Purpose |
| :--- | :--- |
| **[`config.py`](file:///d:/OCR%20of%20bank%20statement%20----%20new/config.py)** | Central configuration: Cohere API keys, Cloudinary credentials, model names, and server settings. |
| **[`cloudinary_service.py`](file:///d:/OCR%20of%20bank%20statement%20----%20new/cloudinary_service.py)** | Handles downloading images from URLs and fetching sample documents from Cloudinary folders. |
| **[`ocr_service.py`](file:///d:/OCR%20of%20bank%20statement%20----%20new/ocr_service.py)** | Uses PaddleOCR to extract text and calls the Cohere LLM (`command-r-08-2024`) to parse specific financial fields into structured data. |
| **[`visualizer.py`](file:///d:/OCR%20of%20bank%20statement%20----%20new/visualizer.py)** | Generates HTML data tables with Pandas and creates Bar Plots / Pie Charts with Matplotlib. |
| **[`ui.py`](file:///d:/OCR%20of%20bank%20statement%20----%20new/ui.py)** | Builds the Gradio Web UI layout, tab items, controls, styling, and connects user clicks to processing functions. |
| **[`app.py`](file:///d:/OCR%20of%20bank%20statement%20----%20new/app.py)** | Lightweight entry point that launches the web app on `http://127.0.0.1:7860`. |
| **[`run.bat`](file:///d:/OCR%20of%20bank%20statement%20----%20new/run.bat)** | Double-clickable Windows batch launcher using Python 3.10. |

---

## 🔄 How Data Flows Through the App

```
      +-----------------------------+
      |      User Interface         |  (ui.py)
      |   (Upload or Cloudinary)    |
      +--------------+--------------+
                     |
         [Image Files / URLs]
                     |
                     v
      +-----------------------------+
      |         Cloudinary          |  (cloudinary_service.py)
      |      Image Downloader       |
      +--------------+--------------+
                     |
                [PIL Image]
                     |
                     v
      +-----------------------------+
      |       PaddleOCR & LLM       |  (ocr_service.py)
      |   1. PaddleOCR text detect  |
      |   2. Cohere LLM extraction  |
      +--------------+--------------+
                     |
        [Extracted Field: Value]
                     |
                     v
      +-----------------------------+
      |        Visualizer           |  (visualizer.py)
      |   1. HTML Tables (Pandas)   |
      |   2. Charts (Matplotlib)    |
      +--------------+--------------+
                     |
                     v
      +-----------------------------+
      |    Rendered in Browser      |
      +-----------------------------+
```

---

## 🚀 How to Run

Double-click `run.bat` or run:
```bash
py -3.10 app.py
```
Open **`http://127.0.0.1:7860`** in your browser.
