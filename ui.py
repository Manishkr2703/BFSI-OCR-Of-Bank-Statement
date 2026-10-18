import gradio as gr
from config import DOCUMENT_TYPES, PLOT_TYPES
from cloudinary_service import get_random_cloudinary_images
from visualizer import visualize_results

CUSTOM_CSS = """
table { 
    width: 100%; 
    border-collapse: collapse; 
    margin-bottom: 20px; 
    font-family: sans-serif;
}
th, td { 
    border: 1px solid #ddd; 
    padding: 10px 14px; 
    text-align: left; 
}
th { 
    background-color: #2b3945; 
    color: white; 
}
tr:nth-child(even) { 
    background-color: #f8f9fa; 
}
"""

def handle_uploaded_files(document_type, files, plot_type):
    """
    Event handler when user uploads files and clicks 'Process Uploaded Files'.
    """
    if not files:
        return "<p style='color:orange;'>No files uploaded. Please upload document images.</p>", []

    image_sources = []
    for f in files:
        if hasattr(f, 'name'):
            image_sources.append(f.name)
        elif hasattr(f, 'path'):
            image_sources.append(f.path)
        else:
            image_sources.append(str(f))

    tables_html, visualization_images = visualize_results(document_type, image_sources, plot_type, is_url=False)
    return tables_html, visualization_images

def handle_cloudinary_fetch(document_type, num_images, plot_type):
    """
    Event handler when user fetches images from Cloudinary.
    """
    selected_urls, gallery_images, error_msg = get_random_cloudinary_images(document_type, num_images)
    if error_msg:
        return f"<p style='color:orange;'>{error_msg}</p>", [], []

    tables_html, visualization_images = visualize_results(document_type, selected_urls, plot_type, is_url=True)
    return tables_html, visualization_images, gallery_images

def create_ui():
    """
    Constructs and returns the complete Gradio UI application block.
    """
    with gr.Blocks(title="Document OCR, Analysis & Visualization", css=CUSTOM_CSS) as demo:
        gr.Markdown("# 📄 Document OCR, Analysis, and Visualization")
        gr.Markdown("Extract key metrics and visualize financial data from bank statements, salary slips, and P&L statements using PaddleOCR and Cohere LLM.")

        with gr.Row():
            document_type = gr.Radio(
                DOCUMENT_TYPES,
                label="1. Select Document Type",
                value=DOCUMENT_TYPES[0]
            )
            plot_type = gr.Radio(
                PLOT_TYPES,
                label="2. Select Plot Type",
                value=PLOT_TYPES[0]
            )

        with gr.Tabs():
            with gr.TabItem("📁 Upload Files"):
                uploaded_files = gr.File(
                    file_types=["image"],
                    file_count="multiple",
                    label="Upload Document Images"
                )
                upload_submit = gr.Button("Process Uploaded Files", variant="primary")

            with gr.TabItem("☁️ Cloudinary Dataset"):
                num_images = gr.Number(
                    label="Number of Random Images to Fetch",
                    value=1,
                    precision=0
                )
                fetch_button = gr.Button("Fetch and Process Cloudinary Images", variant="primary")
                cloudinary_gallery = gr.Gallery(
                    label="Fetched Images from Cloudinary",
                    columns=2,
                    height="auto"
                )

        gr.Markdown("---")
        gr.Markdown("### 📊 Extracted Information & Visualizations")
        result_html = gr.HTML(label="Extracted Information")
        visualization_output = gr.Gallery(
            label="Visualizations",
            columns=2,
            height="auto"
        )

        # Wire Upload Button
        upload_submit.click(
            handle_uploaded_files,
            inputs=[document_type, uploaded_files, plot_type],
            outputs=[result_html, visualization_output]
        )

        # Wire Cloudinary Fetch Button
        fetch_button.click(
            handle_cloudinary_fetch,
            inputs=[document_type, num_images, plot_type],
            outputs=[result_html, visualization_output, cloudinary_gallery]
        )

    return demo
