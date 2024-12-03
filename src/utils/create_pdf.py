from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from PIL import Image
import os
from datetime import datetime
import json

def create_pdf(book_data_file, images_dir, output_dir=None):
    """Create a PDF from the book images"""
    # Load book data
    with open(book_data_file, 'r', encoding='utf-8') as f:
        book_data = json.load(f)
    
    # Create output directory if not provided
    if output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"output/pdf_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up the PDF
    pdf_path = os.path.join(output_dir, f"{book_data['cover']['title']}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4  # A4 size in points
    
    # Function to add an image as a page
    def add_image_page(image_path):
        if os.path.exists(image_path):
            # Open and resize image to fit A4
            img = Image.open(image_path)
            aspect = img.width / img.height
            
            # Calculate dimensions to fit page while maintaining aspect ratio
            if aspect > (width / height):
                new_width = width
                new_height = width / aspect
            else:
                new_height = height
                new_width = height * aspect
            
            # Center the image on the page
            x = (width - new_width) / 2
            y = (height - new_height) / 2
            
            # Add the image
            c.drawImage(image_path, x, y, new_width, new_height)
            c.showPage()
    
    # Add cover
    cover_path = os.path.join(images_dir, "00_cover.png")
    add_image_page(cover_path)
    
    # Add all pages in order
    for i in range(1, len(book_data['pages']) + 1):
        page_path = os.path.join(images_dir, f"{i:02d}_page.png")
        add_image_page(page_path)
    
    # Save the PDF
    c.save()
    print(f"\nPDF created successfully: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python create_pdf.py <book_data.json> <images_directory>")
        sys.exit(1)
    
    create_pdf(sys.argv[1], sys.argv[2])
