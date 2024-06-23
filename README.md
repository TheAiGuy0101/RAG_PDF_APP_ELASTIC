# PDF RAG Application

This application allows users to upload large PDF files, perform Retrieval-Augmented Generation (RAG), and use a Q&A interface to ask questions about the content.


## Installation

1. Clone the repository:
    git clone https://github.com/TheAiGuy0101/pdf_rag_app.git
    cd pdf_rag_app


2. Create a virtual environment and activate it:
    python -m venv venv
    source venv/bin/activate # On Windows, use venv\Scripts\activate


3. Install the required packages:
    pip install -r requirements.txt


4. Configure Tesseract OCR:
   - Install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract).
   - Make sure the Tesseract executable is in your PATH.

5. Configure Elasticsearch:
   - Install and run Elasticsearch locally or configure it to run on a server.
   - Update `config/elasticsearch.yml` with the appropriate settings.

Configure Poppler:

Windows:

    Download Poppler for Windows from Poppler download [link](https://github.com/oschwartz10612/poppler-windows/releases/tag/v24.02.0-0) for Windows.
    Extract the contents of the downloaded ZIP file to a directory, e.g., C:\poppler-xx.
    Add the bin directory to your system's PATH:
    Open the Start Search, type in "env", and select "Edit the system environment variables."
    Click the "Environment Variables" button.
    In the "System variables" section, find the Path variable and click "Edit."
    Click "New" and add the path to the Poppler bin directory, e.g., C:\poppler-xx\bin.
    Click OK to close all the dialogs.

7. Add your OpenAI API key to `config/openai.yml`.

## Running the Application
    streamlit run src/main.py

## Usage

- Upload PDF files using the provided file uploader.
- The application will process the PDFs and index the text in Elasticsearch.
- Use the Q&A interface to ask questions about the content of the PDFs.

## Notes

- Ensure you have Tesseract OCR installed and correctly configured for your operating system.
- Adjust the Elasticsearch configuration as necessary for your environment.
- The OpenAI API key should be securely stored and not hard-coded in your scripts.
