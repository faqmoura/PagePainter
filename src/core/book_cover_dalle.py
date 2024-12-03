from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import os
import io
import requests
from dotenv import load_dotenv
from datetime import datetime

class BookCover:
    def __init__(self):
        """Initialize the BookCover generator with DALL-E 3"""
        # Load environment variables
        load_dotenv()
        
        # Initialize OpenAI client
        self.client = OpenAI()

    def generate_cover(self, book_data, description, output_path, art_style=None):
        """Generate a book cover with title and illustration"""
        try:
            # Create the complete prompt with art style
            if art_style:
                prompt = f"{art_style}, {description}"
            else:
                prompt = f"children's book cover illustration, watercolor style, {description}"
            
            print(f"\nGenerating cover illustration with prompt: {prompt[:100]}...")
            
            # Generate image with DALL-E 3
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            # Get the image URL
            image_url = response.data[0].url
            
            # Download the image
            response = requests.get(image_url)
            image = Image.open(io.BytesIO(response.content))
            
            # Create a new canvas for the cover
            canvas_width = 1200
            canvas_height = 1600
            canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
            
            # Resize and paste the illustration
            image_height = int(canvas_height * 0.7)  # 70% for image
            resized_image = image.resize((canvas_width, image_height))
            canvas.paste(resized_image, (0, 0))
            
            # Add text
            draw = ImageDraw.Draw(canvas)
            
            # Try to use Comic Sans MS, fall back to Arial, then default
            try:
                title_font = ImageFont.truetype("comic.ttf", 120)  # Larger size for title
                subtitle_font = ImageFont.truetype("comic.ttf", 60)  # Smaller size for other text
            except:
                try:
                    title_font = ImageFont.truetype("arial.ttf", 120)
                    subtitle_font = ImageFont.truetype("arial.ttf", 60)
                except:
                    title_font = ImageFont.load_default()
                    subtitle_font = ImageFont.load_default()
            
            # Center the title text
            title = book_data['title']
            title_width = draw.textlength(title, font=title_font)
            title_x = (canvas_width - title_width) / 2
            title_y = image_height + 50  # Add some padding from the image
            
            # Draw title with shadow effect
            shadow_offset = 3
            draw.text((title_x + shadow_offset, title_y + shadow_offset), title, font=title_font, fill='grey')
            draw.text((title_x, title_y), title, font=title_font, fill='black')
            
            # Add author text
            if 'author' in book_data:
                author_text = f"por {book_data['author']}"
                author_width = draw.textlength(author_text, font=subtitle_font)
                author_x = (canvas_width - author_width) / 2
                author_y = title_y + title_font.size + 30
                draw.text((author_x, author_y), author_text, font=subtitle_font, fill='black')
            
            # Add illustrator text
            if 'illustrator' in book_data:
                illustrator_text = f"Ilustrações por {book_data['illustrator']}"
                illustrator_width = draw.textlength(illustrator_text, font=subtitle_font)
                illustrator_x = (canvas_width - illustrator_width) / 2
                illustrator_y = title_y + title_font.size + subtitle_font.size + 60
                draw.text((illustrator_x, illustrator_y), illustrator_text, font=subtitle_font, fill='black')
            
            # Add year
            year = datetime.now().year
            year_text = str(year)
            year_width = draw.textlength(year_text, font=subtitle_font)
            year_x = (canvas_width - year_width) / 2
            year_y = canvas_height - subtitle_font.size - 30
            draw.text((year_x, year_y), year_text, font=subtitle_font, fill='black')
            
            # Save the cover
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            canvas.save(output_path)
            return canvas
            
        except Exception as e:
            print(f"Error generating cover: {str(e)}")
            # Create a placeholder cover
            canvas = Image.new('RGB', (1200, 1600), color='white')
            draw = ImageDraw.Draw(canvas)
            draw.text((10, 10), "Cover generation failed", fill='black')
            draw.text((10, 30), f"Error: {str(e)}", fill='black')
            draw.text((10, 60), book_data['title'], fill='black')
            
            # Save the placeholder
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            canvas.save(output_path)
            return canvas
