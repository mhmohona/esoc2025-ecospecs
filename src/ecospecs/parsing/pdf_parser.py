import pdfplumber
from typing import List

def parse_pdf_tables(file_path: str) -> List[List[List[str]]]:
    """Extract tables from PDF file"""
    try:
        with pdfplumber.open(file_path) as pdf:
            return [
                table.extract()
                for page in pdf.pages
                for table in page.extract_tables()
            ]
    except Exception as e:
        raise RuntimeError(f"PDF parsing failed: {str(e)}") from e