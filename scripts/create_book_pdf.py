import os
from src.utils.create_pdf import create_pdf

# Configuration
BOOK_DIR = "output/book_O Papai Coruja_20241129_103150"  # Updated to use the specified folder
BOOK_JSON = "examples/papai_coruja.json"  # Updated path to examples directory

# Create PDF
print("\nCreating PDF with all pages...")
pdf_path = create_pdf(BOOK_JSON, BOOK_DIR)
print(f"PDF created at: {pdf_path}")
