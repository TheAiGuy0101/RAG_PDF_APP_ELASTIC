import pytesseract
from pdf2image import convert_from_path
import concurrent.futures
import logging

logger = logging.getLogger(__name__)

def pdf_to_text(pdf_path):
    try:
        logger.info(f"Starting PDF to text conversion for {pdf_path}")
        pages = convert_from_path(pdf_path, 300)
        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page)
        logger.info(f"Completed PDF to text conversion for {pdf_path}")
        return text
    except Exception as e:
        logger.error(f"Error converting PDF to text for {pdf_path}: {e}")
        raise

def process_pdf(file_path):
    return pdf_to_text(file_path)

def process_files_in_parallel(file_paths):
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(process_pdf, file_paths))
        return results
    except Exception as e:
        logger.error(f"Error processing files in parallel: {e}")
        raise
