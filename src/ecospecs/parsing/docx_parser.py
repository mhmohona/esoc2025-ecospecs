from docx import Document
from typing import List

def parse_docx_tables(file_path: str) -> List[List[List[str]]]:
    """Extract tables from DOCX file"""
    try:
        doc = Document(file_path)
        return [
            [
                [cell.text.strip() for cell in row.cells]
                for row in table.rows
            ]
            for table in doc.tables
        ]
    except Exception as e:
        raise RuntimeError(f"DOCX parsing failed: {str(e)}") from e