import json
import os
from datetime import datetime
from src.core.book_cover_dalle import BookCover

def generate_cover(book_data_file):
    """Generate just the book cover from the provided JSON data file"""
    print("Initializing cover generator...")
    
    # Load book data
    print(f"Loading book data from {book_data_file}...")
    with open(book_data_file, 'r', encoding='utf-8') as f:
        book_data = json.load(f)
    
    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output/cover_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nCreating cover in directory: {output_dir}")
    
    # Generate cover
    print("\nGenerating book cover...")
    cover_generator = BookCover()
    cover_path = os.path.join(output_dir, "cover.png")
    cover_generator.generate_cover(
        book_data['cover'],
        book_data['cover'].get('style_override', book_data['book_settings'].get('art_style', '')),
        cover_path,
        book_data['book_settings'].get('art_style')
    )
    print(f"Cover saved as: {cover_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python generate_cover.py <book_data.json>")
        sys.exit(1)
    
    generate_cover(sys.argv[1])
