import unittest
import os
from src.utils.create_pdf import create_pdf

class TestPDFGenerator(unittest.TestCase):
    def setUp(self):
        self.test_book_json = "examples/example_book.json"
        self.test_output_dir = "output/test_pdf"
        os.makedirs(self.test_output_dir, exist_ok=True)

    def test_pdf_creation(self):
        # Test if PDF creation function returns a path
        pdf_path = create_pdf(self.test_book_json, self.test_output_dir)
        self.assertIsInstance(pdf_path, str)
        
        # Test if the PDF file was actually created
        self.assertTrue(os.path.exists(pdf_path))

if __name__ == '__main__':
    unittest.main()
