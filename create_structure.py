import os
import shutil

# Create directory structure
directories = [
    'src/backends',
    'src/core',
    'src/utils',
    'examples',
    'scripts',
    'tests'
]

for dir_path in directories:
    os.makedirs(dir_path, exist_ok=True)
    print(f"Created directory: {dir_path}")

# Define file movements
file_moves = {
    'src/backends/': [
        'page_painter_dalle.py',
        'page_painter_gemini.py',
        'page_painter_dreamstudio.py',
        'page_painter_opensource.py'
    ],
    'src/core/': [
        'book_cover_dalle.py',
        'book_cover_gemini.py',
        'book_cover_dreamstudio.py',
        'book_cover_opensource.py',
        'page_painter.py'
    ],
    'src/utils/': [
        'create_pdf.py'
    ],
    'examples/': [
        'example_book.json',
        'papai_coruja.json'
    ],
    'scripts/': [
        'generate_book_dalle.py',
        'generate_book_gemini.py',
        'generate_book_dreamstudio.py',
        'generate_book_opensource.py',
        'create_book_pdf.py',
        'generate_cover.py'
    ]
}

# Move files to their new locations
for dir_path, files in file_moves.items():
    for file_name in files:
        if os.path.exists(file_name):
            dest_path = os.path.join(dir_path, file_name)
            shutil.move(file_name, dest_path)
            print(f"Moved {file_name} to {dest_path}")
        else:
            print(f"Warning: {file_name} not found")

print("\nProject structure created successfully!")
