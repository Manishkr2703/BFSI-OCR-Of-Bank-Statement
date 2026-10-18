"""
Document OCR, Analysis, and Visualization
Main entry point for the application.
"""
from ui import create_ui
from config import SERVER_NAME, SERVER_PORT

def main():
    print(f"Launching Document OCR App at http://{SERVER_NAME}:{SERVER_PORT} ...")
    demo = create_ui()
    demo.launch(
        server_name=SERVER_NAME,
        server_port=SERVER_PORT,
        inbrowser=True
    )

if __name__ == "__main__":
    main()