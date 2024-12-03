# PagePainter - AI Children's Book Generator

PagePainter is a Python-based tool that automatically generates illustrated children's books using various AI image generation models. It supports multiple backends including DALL-E 3, DreamStudio, and open-source models.

This project was inspired by [Fable Forge](https://github.com/fable-forge/fable-forge), expanding upon its concepts to create a versatile tool for children's book generation.

## Features

- Multiple AI image generation backends:
  - DALL-E 3 (OpenAI)
  - DreamStudio (Stability AI)
  - Open-source models (Stable Diffusion)
- Customizable book styling and layout
- PDF generation with proper formatting
- Support for multiple languages
- Configurable image generation parameters
- Book cover generation with title, author, and illustrator information

## Backend Comparison

### DALL-E 3
- **Quality**: Best results among all backends
- **Speed**: Fast generation (seconds per image)
- **Cost**: Paid service (~$0.40 for a 10-page book)
- **Pros**: High-quality illustrations, consistent style, fast generation
- **Cons**: Not free

### DreamStudio
- **Quality**: Moderate results
- **Speed**: Fast generation
- **Cost**: Paid service but offers free credits
- **Pros**: Free credits available, fast generation
- **Cons**: Image quality not as good as DALL-E 3

### Stable Diffusion (CPU)
- **Quality**: Basic results (may improve with more iterations)
- **Speed**: Very slow on CPU (~7 minutes per page)
- **Cost**: Free (self-hosted)
- **Pros**: Free, fully customizable
- **Cons**: Slow on CPU, requires optimization for better results

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PagePainter.git
cd PagePainter
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root and add your API keys:
```
OPENAI_API_KEY=your_openai_key
STABILITY_API_KEY=your_dreamstudio_key
```

## Usage

1. Create a book configuration file (see `example_book.json` for reference)

2. Generate a book using your preferred backend:

```bash
# Using DALL-E 3
python scripts/run_with_path.py generate_book_dalle.py your_book.json

# Using DreamStudio
python scripts/run_with_path.py generate_book_dreamstudio.py your_book.json

# Using open-source model
python scripts/run_with_path.py generate_book_opensource.py your_book.json
```

3. Generate PDF:
```bash
python scripts/run_with_path.py create_book_pdf.py your_book.json
```

## Project Structure

```
PagePainter/
├── src/                    # Source code
│   ├── backends/          # Image generation backends
│   │   ├── dalle.py
│   │   ├── dreamstudio.py
│   │   └── opensource.py
│   ├── core/             # Core functionality
│   │   ├── page_painter.py
│   │   └── book_cover.py
│   └── utils/            # Utility functions
│       ├── pdf_generator.py
│       └── image_utils.py
├── examples/             # Example books and configurations
│   ├── example_book.json
│   └── papai_coruja.json
├── scripts/             # Generation scripts
│   ├── generate_book.py
│   └── create_pdf.py
├── tests/              # Unit tests
├── .env               # Environment variables
├── .gitignore        # Git ignore file
├── requirements.txt  # Project dependencies
└── README.md        # Project documentation
```

## Configuration

The book configuration file (`your_book.json`) supports the following parameters:

```json
{
    "book_settings": {
        "language": "en",
        "art_style": "watercolor children's book style"
    },
    "cover": {
        "title": "Your Book Title",
        "author": "Author Name",
        "illustrator": "PagePainter AI",
        "style_override": "custom style for cover"
    },
    "pages": [
        {
            "text": "Page text",
            "description": "Scene description for AI",
            "style_override": null
        }
    ]
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for DALL-E 3
- Stability AI for DreamStudio
- The Stable Diffusion community
- [Fable Forge](https://github.com/fable-forge/fable-forge) project for inspiration

## Authors

- Felippe Moura - Initial work
