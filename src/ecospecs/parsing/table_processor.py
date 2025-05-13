from pathlib import Path
from .docx_parser import parse_docx_tables
from .pdf_parser import parse_pdf_tables

def process_file(file_path: str) -> list:
    """Main entry point for table parsing"""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if path.suffix.lower() == '.docx':
        return parse_docx_tables(file_path)
    elif path.suffix.lower() == '.pdf':
        return parse_pdf_tables(file_path)
    
    raise ValueError(f"Unsupported file format: {path.suffix}")