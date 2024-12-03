import json
import os
from book_cover_opensource import BookCover
from page_painter_opensource import PagePainter
from datetime import datetime

class BookGenerator:
    def __init__(self):
        """Initialize the book generator with cover and page makers"""
        print("Initializing book generator...")
        self.cover_maker = BookCover()
        self.page_maker = PagePainter()

    def create_book_directory(self, book_title):
        """Create a directory for the book's files"""
        # Create a safe filename from the title
        safe_title = "".join(x for x in book_title if x.isalnum() or x in (' ', '-', '_')).rstrip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_name = f"output/book_{safe_title}_{timestamp}"
        
        os.makedirs(dir_name, exist_ok=True)
        return dir_name

    def generate_book(self, json_path):
        """Generate a complete book from JSON specification"""
        # Load book data
        print(f"Loading book data from {json_path}...")
        with open(json_path, 'r', encoding='utf-8') as f:
            book_data = json.load(f)

        # Get book settings
        book_settings = book_data.get('book_settings', {})
        default_style = book_settings.get('art_style', "watercolor painting, soft colors, children's book style")
        image_size = book_settings.get('image_size', {"width": 384, "height": 512})

        # Create book directory
        book_dir = self.create_book_directory(book_data['cover']['title'])
        print(f"Creating book in directory: {book_dir}")

        # Generate cover
        print("\nGenerating book cover...")
        cover_info = book_data['cover']
        other_info = [
            f"Written by {cover_info['author']}",
            f"Illustrated by {cover_info['illustrator']}"
        ]
        other_info.extend(cover_info.get('additional_info', []))
        
        cover_path = os.path.join(book_dir, "00_cover.png")
        # Use cover style override if provided, else use default style
        cover_style = cover_info.get('style_override', default_style)
        self.cover_maker.create_cover(
            title=cover_info['title'],
            other_info=other_info,
            output_path=cover_path,
            art_style=cover_style,
            image_size=image_size
        )
        print(f"Cover saved as: {cover_path}")

        # Generate pages
        print("\nGenerating book pages...")
        for i, page in enumerate(book_data['pages'], 1):
            print(f"\nGenerating page {i}...")
            page_path = os.path.join(book_dir, f"{i:02d}_page.png")
            
            # Use page style override if provided, else use default style
            page_style = page.get('style_override', default_style)
            
            self.page_maker.create_book_page(
                text=page['text'],
                description=page['description'],
                output_path=page_path,
                art_style=page_style,
                image_size=image_size
            )
            print(f"Page {i} saved as: {page_path}")

        print(f"\nBook generation complete! All files are in: {book_dir}")
        return book_dir

def main():
    # Check if JSON file is provided as argument
    import sys
    if len(sys.argv) != 2:
        print("Usage: python generate_book_opensource.py <path_to_book_json>")
        print("Example: python generate_book_opensource.py example_book.json")
        sys.exit(1)

    json_path = sys.argv[1]
    if not os.path.exists(json_path):
        print(f"Error: File not found: {json_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Generate the book
    generator = BookGenerator()
    generator.generate_book(json_path)

if __name__ == "__main__":
    main()
