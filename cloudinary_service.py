import io
import random
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import cloudinary
import cloudinary.api
from config import CLOUDINARY_CONFIG, CLOUDINARY_FOLDER_MAPPING

# Initialize Cloudinary configuration once
cloudinary.config(
    cloud_name=CLOUDINARY_CONFIG["cloud_name"],
    api_key=CLOUDINARY_CONFIG["api_key"],
    api_secret=CLOUDINARY_CONFIG["api_secret"]
)

def download_image_from_url(url):
    """
    Download an image from a URL and return a PIL Image object.
    """
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return None

def fetch_from_cloudinary(folder_prefix):
    """
    Fetch image URLs from Cloudinary matching the given folder prefix.
    """
    try:
        response = cloudinary.api.resources(
            type="upload",
            prefix=folder_prefix,
            resource_type="image",
            max_results=100
        )
        return [resource["secure_url"] for resource in response.get("resources", [])]
    except Exception as e:
        return f"Failed to fetch files from Cloudinary: {e}"

def get_random_cloudinary_images(document_type, num_images):
    """
    Get a random sample of images from Cloudinary for a given document type.
    Returns: (selected_urls, gallery_images, error_message)
    """
    if not document_type:
        return [], [], "Please select a document type."

    folder_name = CLOUDINARY_FOLDER_MAPPING.get(document_type)
    if folder_name is None:
        supported = ", ".join(f"'{k}'" for k in CLOUDINARY_FOLDER_MAPPING.keys())
        return [], [], f"Cloudinary dataset currently supports: {supported}. For '{document_type}', please upload files in the 'Upload Files' tab."

    urls = fetch_from_cloudinary(folder_name)
    if isinstance(urls, str):  # Error string returned
        return [], [], urls

    if not urls:
        return [], [], "No images found in Cloudinary for the selected document type."

    sample_count = max(1, min(len(urls), int(num_images or 1)))
    selected_urls = random.sample(urls, sample_count)

    gallery_images = []
    for url in selected_urls:
        img = download_image_from_url(url)
        if img is not None:
            gallery_images.append(np.array(img))

    return selected_urls, gallery_images, None
