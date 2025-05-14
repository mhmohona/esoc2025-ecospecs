import os
import pytest
from pathlib import Path
from parsing.table_processor import process_file

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Sample test data path
TEST_DATA_DIR = Path(__file__).parent / "test_data"

# Sample test files (assumed to be in test_data)
DOCX_TEST_FILE = TEST_DATA_DIR / "A_1_test.docx"
PDF_TEST_FILE = TEST_DATA_DIR / "sample_test.pdf"

def test_parse_docx_file():
    """Test parsing tables from a .docx file."""
    tables = process_file(DOCX_TEST_FILE)
    assert isinstance(tables, list), "Output should be a list of tables"
    assert len(tables) > 0, "Should parse at least one table"
    
    # Verify the structure of the first table (based on A_1.docx's first table)
    expected_first_table = [
        ["Revisions-Nr.", "Änderungsgrund", "Datum (TT.MM.JJJJ)"],
        ["01", "Erstellung", "20.03.2025"]
    ]
    assert tables[0] == expected_first_table, "First table content mismatch"

def test_empty_file():
    """Test parsing an empty or non-existent file."""
    empty_file = TEST_DATA_DIR / "empty.docx"
    with pytest.raises(Exception):
        process_file(empty_file)

def test_file_with_no_tables():
    """Test parsing a file with no tables."""
    no_tables_file = TEST_DATA_DIR / "no_tables.docx"
    tables = process_file(no_tables_file)
    assert len(tables) == 0, "Should return empty list for file with no tables"

# Optional: Test malformed table if applicable
def test_malformed_table():
    """Test parsing a file with a malformed table."""
    malformed_file = TEST_DATA_DIR / "malformed_table.docx"
    tables = process_file(malformed_file)
    assert len(tables) > 0, "Should still parse available tables"
    # Add specific checks if malformed table handling is defined