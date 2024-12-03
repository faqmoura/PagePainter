import os
from PIL import Image, ImageDraw, ImageFont
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from stability_sdk import client
import io
import warnings
from dotenv import load_dotenv

class PagePainter:
    def __init__(self):
        """Initialize the PagePainter with the Stability API"""
        # Load environment variables
        load_dotenv()
        
        # Get API key from environment variable
        api_key = os.getenv('STABILITY_KEY')
        if not api_key:
            raise ValueError("Please set STABILITY_KEY environment variable")
        
        # Initialize the stability client
        self.stability_api = client.StabilityInference(
            key=api_key,
            verbose=False,
        )
        
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
    
    def generate_illustration(self, description, art_style=None, image_size=None):
        """Generate an illustration based on the description and art style"""
        # Set default image size if not provided
        if image_size is None:
            image_size = {"width": 384, "height": 512}
            
        # Create the complete prompt with art style
        if art_style:
            prompt = f"{art_style}, {description}"
        else:
            # Default style if none provided
            prompt = f"watercolor style illustration, children's book style, {description}"
        
        # Generate the image
        answers = self.stability_api.generate(
            prompt=prompt,
            seed=42,  # Change this for different results
            steps=30,
            cfg_scale=7.5,
            width=image_size["width"],
            height=image_size["height"],
            samples=1,
            sampler=generation.SAMPLER_K_DPMPP_2M
        )
        
        # Process the first (and only) result
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                    return None
                if artifact.type == generation.ARTIFACT_IMAGE:
                    # Convert binary image data to PIL Image
                    img = Image.open(io.BytesIO(artifact.binary))
                    return img
        
        return None

    def create_page(self, text, image, output_path):
        """Create a book page with text and illustration"""
        # Create a new white canvas
        canvas_width = 1200
        canvas_height = 1600
        canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
        
        # Resize and paste the illustration
        illustration_height = int(canvas_height * 0.7)  # Leave space for text
        illustration_width = canvas_width
        resized_image = image.resize((illustration_width, illustration_height))
        canvas.paste(resized_image, (0, 0))
        
        # Add text
        draw = ImageDraw.Draw(canvas)
        
        # Try to use Arial Unicode MS or a similar font that supports accents
        font_paths = [
            "C:/Windows/Fonts/ARIALUNI.TTF",  # Arial Unicode MS
            "C:/Windows/Fonts/arial.ttf",      # Regular Arial
            "C:/Windows/Fonts/segoeui.ttf",    # Segoe UI
            "C:/Windows/Fonts/calibri.ttf",    # Calibri
        ]
        
        font = None
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, 40)
                    break
            except Exception:
                continue
                
        if font is None:
            # Fallback to default font if none of the above work
            font = ImageFont.load_default()
            print("Warning: Using default font. Text accents might not display correctly.")
        
        # Text area dimensions
        text_area_width = canvas_width - 100  # 50px margin on each side
        text_area_height = canvas_height - illustration_height - 100  # 50px margin top and bottom
        text_start_y = illustration_height + 50
        
        # Word wrap text
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            # Check if the line is too long
            if draw.textlength(test_line, font=font) > text_area_width:
                if len(current_line) > 1:
                    # Remove the last word and store the line
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # If a single word is too long, keep it as its own line
                    lines.append(test_line)
                    current_line = []
        
        # Add any remaining words as the last line
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw text lines
        y = text_start_y
        for line in lines:
            # Center each line
            text_width = draw.textlength(line, font=font)
            x = (canvas_width - text_width) / 2
            # Use 'utf-8' encoding for text
            draw.text((x, y), line, font=font, fill='black')
            y += int(font.size * 1.5)  # Add some line spacing
        
        # Save the final page
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        canvas.save(output_path)
        return canvas

    def create_book_page(self, text, description, output_path, art_style=None, image_size=None):
        """Create a complete book page with illustration and text"""
        # Generate the illustration
        image = self.generate_illustration(description, art_style, image_size)
        if image is None:
            raise ValueError("Failed to generate illustration")
        
        # Add text to the image
        self.create_page(text, image, output_path)
