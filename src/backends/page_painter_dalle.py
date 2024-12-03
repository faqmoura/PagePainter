from openai import OpenAI
from PIL import Image
import os
import io
import requests
from dotenv import load_dotenv

class PagePainter:
    def __init__(self):
        """Initialize the PagePainter with DALL-E 3"""
        # Load environment variables
        load_dotenv()
        
        # Initialize OpenAI client
        self.client = OpenAI()
        
    def generate_illustration(self, description, art_style=None, image_size=None):
        """Generate an illustration using DALL-E 3"""
        try:
            # Set default image size if not provided
            if image_size is None:
                image_size = {"width": 1024, "height": 1024}
                
            # Create the complete prompt with art style
            if art_style:
                prompt = f"{art_style}, {description}"
            else:
                # Default style if none provided
                prompt = f"watercolor style illustration, children's book style, {description}"
            
            print(f"\nGenerating illustration with prompt: {prompt[:100]}...")
            
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
            
            return image
            
        except Exception as e:
            print(f"Error generating illustration: {str(e)}")
            # Create a placeholder image
            img = Image.new('RGB', (image_size["width"], image_size["height"]), color='white')
            d = ImageDraw.Draw(img)
            d.text((10, 10), "Image generation failed", fill='black')
            d.text((10, 30), f"Error: {str(e)}", fill='black')
            return img
    
    def create_page(self, text, image, output_path):
        """Create a page combining the illustration and text"""
        # Create a new white canvas
        canvas_width = 1200
        canvas_height = 1600
        canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
        
        # Resize the illustration to fit the top portion
        image_height = int(canvas_height * 0.7)  # 70% for image
        resized_image = image.resize((canvas_width, image_height))
        
        # Paste the illustration
        canvas.paste(resized_image, (0, 0))
        
        # Add text
        draw = ImageDraw.Draw(canvas)
        
        # Try to use Comic Sans MS, fall back to Arial, then default if neither is available
        try:
            font = ImageFont.truetype("comic.ttf", 72)  # Comic Sans MS with larger size
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 72)
            except:
                font = ImageFont.load_default()
        
        # Text area dimensions
        text_area_height = canvas_height - image_height
        text_margin = 80  # Increased margin
        
        # Word wrap for text
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            text_width = draw.textlength(' '.join(current_line), font=font)
            if text_width > canvas_width - 2 * text_margin:
                if len(current_line) == 1:
                    lines.append(current_line[0])
                    current_line = []
                else:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate total text height
        line_spacing = 1.2  # 120% of font size
        total_text_height = len(lines) * font.size * line_spacing
        
        # Calculate starting Y position to center text vertically in the text area
        start_y = image_height + (text_area_height - total_text_height) / 2
        
        # Draw each line of text
        for i, line in enumerate(lines):
            # Center text horizontally
            text_width = draw.textlength(line, font=font)
            x = (canvas_width - text_width) / 2
            y = start_y + i * font.size * line_spacing
            
            # Draw text with a slight shadow effect for better readability
            shadow_offset = 2
            draw.text((x + shadow_offset, y + shadow_offset), line, font=font, fill='grey')
            draw.text((x, y), line, font=font, fill='black')
        
        # Save the final page
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        canvas.save(output_path)
        return canvas

    def create_book_page(self, text, description, output_path, art_style=None, image_size=None):
        """Create a complete book page with illustration and text"""
        # Generate the illustration
        image = self.generate_illustration(description, art_style, image_size)
        
        # Add text to the image
        self.create_page(text, image, output_path)
