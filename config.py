import os
import cloudinary

# ==========================================
# 1. Cohere API Configuration
# ==========================================
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "use your own api key ")
COHERE_MODEL = "command-r-08-2024"

# ==========================================
# 2. Cloudinary Storage Configuration
# ==========================================
CLOUDINARY_CONFIG = {
    "cloud_name": os.getenv("CLOUDINARY_CLOUD_NAME", "use your own"),
    "api_key": os.getenv("CLOUDINARY_API_KEY", "use your own "),
    "api_secret": os.getenv("CLOUDINARY_API_SECRET", "use your own "),
}

# Mapping between Document Type and Cloudinary folder name
CLOUDINARY_FOLDER_MAPPING = {
    "Profit and Loss Statement": "dataset1/profit and loss",
    "Salary Slip": "dataset1/salary slip"
}

# ==========================================
# 3. Application Options & Settings
# ==========================================
DOCUMENT_TYPES = ["Salary Slip", "Profit and Loss Statement", "Check"]
PLOT_TYPES = ["Bar Plot", "Pie Chart"]

SERVER_NAME = "127.0.0.1"
SERVER_PORT = 7860
