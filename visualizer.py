import io
import re
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
from ocr_service import process_documents

def extract_numeric_data(data_dict):
    """
    Extracts numeric values from a dictionary of extracted fields,
    filtering out non-numeric error messages.
    """
    numeric_data = {}
    for key, value in data_dict.items():
        if key == "Error":
            continue
        try:
            cleaned_number = re.sub(r"[^\d.]+", "", str(value))
            if cleaned_number:
                numeric_data[key] = float(cleaned_number)
        except ValueError:
            pass
    return numeric_data

def generate_chart(numeric_data, document_type, image_idx, plot_type):
    """
    Generates a Matplotlib figure (Bar Plot or Pie Chart) and converts it to a PIL Image.
    """
    if not numeric_data:
        # Return a blank placeholder image if no numeric values could be plotted
        return Image.new("RGB", (300, 200), color=(255, 255, 255))

    fig, ax = plt.subplots(figsize=(10, 6))
    labels = list(numeric_data.keys())
    values = list(numeric_data.values())

    if plot_type == "Bar Plot":
        ax.bar(labels, values, color="skyblue", edgecolor="black")
        ax.set_title(f"{document_type} - Image {image_idx + 1} - Bar Plot")
        ax.set_ylabel("Amount")
        ax.set_xlabel("Fields")
        plt.xticks(rotation=45, ha="right")

    elif plot_type == "Pie Chart":
        ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=140,
            colors=plt.cm.Paired.colors
        )
        ax.set_title(f"{document_type} - Image {image_idx + 1} - Pie Chart")

    # Render figure into PIL Image in memory
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    chart_image = Image.open(buf)
    plt.close(fig)  # Always close the figure to avoid memory leaks

    return chart_image

def visualize_results(document_type, image_sources, plot_type, is_url=False):
    """
    Coordinates document processing, creates HTML tables for extracted data,
    and generates visual charts for each image.
    """
    if not image_sources:
        return "<p style='color:orange;'>No files provided. Please upload images or fetch from Cloudinary.</p>", []

    extracted_data = process_documents(document_type, image_sources, is_url)

    if not extracted_data:
        return "<p style='color:orange;'>No data extracted. Please check your input files.</p>", []

    tables_html = ""
    visualization_images = []

    for idx, data in enumerate(extracted_data):
        if data:
            df = pd.DataFrame(list(data.items()), columns=["Field", "Value"])
            tables_html += f"<h4>Extracted Information for Image {idx + 1}</h4>"
            tables_html += df.to_html(index=False, escape=False, border=0)

            numeric_data = extract_numeric_data(data)
            chart_img = generate_chart(numeric_data, document_type, idx, plot_type)
            visualization_images.append(chart_img)
        else:
            tables_html += f"<h4>Image {idx + 1}</h4><p>No data extracted from this image.</p>"
            blank_image = Image.new("RGB", (300, 200), color=(255, 255, 255))
            visualization_images.append(blank_image)

    return tables_html, visualization_images
