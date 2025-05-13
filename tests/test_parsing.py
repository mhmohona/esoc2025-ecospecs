import pytest
from src.ecospecs.parsing.table_processor import process_file

def test_docx_parsing():
    tables = process_file("tests/test_data/sample.docx")
    assert len(tables) > 0
    assert len(tables[0]) > 0

def test_pdf_parsing():
    tables = process_file("tests/test_data/sample.pdf")
    assert len(tables) > 0
    assert len(tables[0]) > 0

def test_invalid_file():
    with pytest.raises(FileNotFoundError):
        process_file("non_existent.docx")