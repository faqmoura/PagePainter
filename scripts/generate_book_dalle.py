import os
import json
from datetime import datetime
from src.backends.page_painter_dalle import PagePainter
from src.core.book_cover_dalle import BookCover

def generate_book(book_data_file):
    """Generate a complete book from the provided JSON data file"""
    print("Initializing book generator...")
    
    # Load book data
    print(f"Loading book data from {book_data_file}...")
    with open(book_data_file, 'r', encoding='utf-8') as f:
        book_data = json.load(f)
    
    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    book_dir = f"output/book_{book_data['cover']['title']}_{timestamp}"
    os.makedirs(book_dir, exist_ok=True)
    
    print(f"\nCreating book in directory: {book_dir}")
    
    # Generate cover
    print("\nGenerating book cover...")
    cover_generator = BookCover()
    cover_path = os.path.join(book_dir, "00_cover.png")
    cover_generator.generate_cover(
        book_data['cover'],
        book_data['cover'].get('style_override', book_data['book_settings'].get('art_style', '')),
        cover_path,
        book_data['book_settings'].get('art_style')
    )
    print(f"Cover saved as: {cover_path}")
    
    # Generate pages
    print("\nGenerating book pages...")
    page_generator = PagePainter()
    
    for i, page in enumerate(book_data['pages'], 1):
        print(f"\nGenerating page {i}...")
        page_path = os.path.join(book_dir, f"{i:02d}_page.png")
        
        # Use style_override if available, otherwise use book's default art style
        style = page.get('style_override', book_data['book_settings'].get('art_style'))
        
        page_generator.create_book_page(
            page['text'],
            page['description'],
            page_path,
            style,
            book_data['book_settings'].get('image_size')
        )
        print(f"Page {i} saved as: {page_path}")
    
    print(f"\nBook generation complete! All files are in: {book_dir}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python generate_book_dalle.py <book_data.json>")
        sys.exit(1)
    
    generate_book(sys.argv[1])
