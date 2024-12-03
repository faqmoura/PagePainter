from page_painter import PagePainter
import os

def main():
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Initialize PagePainter
    painter = PagePainter()
    
    # Example text and description
    text = "Once upon a time, there was a little rabbit who loved to paint rainbows."
    description = "A cute white rabbit holding a paintbrush, painting a rainbow in a garden"
    
    # Generate the page
    output_path = "output/page1.png"
    painter.create_book_page(text, description, output_path)
    print(f"Page created successfully! Check {output_path}")

if __name__ == "__main__":
    main()
