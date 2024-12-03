import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from stability_sdk import client
import io
import warnings
from dotenv import load_dotenv

class BookCover:
    def __init__(self):
        """Initialize the BookCover with the Stability API"""
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
    
    def generate_cover_image(self, title, art_style=None, image_size=None):
        """Generate the cover illustration based on the title"""
        # Set default image size if not provided
        if image_size is None:
            image_size = {"width": 384, "height": 512}
            
        # Create the prompt with art style
        if art_style:
            prompt = f"{art_style}, book cover illustration of {title}, professional book cover art"
        else:
            prompt = f"watercolor style illustration, children's book style, book cover illustration of {title}, professional book cover art"
        
        # Set up the generation parameters
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

    def add_text_to_cover(self, image, title, other_info):
        """Add title and other text to the cover image"""
        # Create a new canvas with the same size as the image
        canvas = Image.new('RGB', image.size, 'white')
        canvas.paste(image)
        draw = ImageDraw.Draw(canvas)

        # Try to use Arial Unicode MS or a similar font that supports accents
        font_paths = [
            "C:/Windows/Fonts/ARIALUNI.TTF",  # Arial Unicode MS
            "C:/Windows/Fonts/arial.ttf",      # Regular Arial
            "C:/Windows/Fonts/segoeui.ttf",    # Segoe UI
            "C:/Windows/Fonts/calibri.ttf",    # Calibri
        ]
        
        title_font = None
        info_font = None
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    title_font = ImageFont.truetype(font_path, 60)
                    info_font = ImageFont.truetype(font_path, 30)
                    break
            except Exception:
                continue
                
        if title_font is None:
            # Fallback to default font if none of the above work
            title_font = info_font = ImageFont.load_default()
            print("Warning: Using default font. Text accents might not display correctly.")

        # Add title at the top
        title_width = draw.textlength(title, font=title_font)
        x = (image.width - title_width) / 2
        y = 50
        draw.text((x, y), title, font=title_font, fill='black')

        # Add other info at the bottom
        y = image.height - 50 - (len(other_info) * 40)
        for info in other_info:
            info_width = draw.textlength(info, font=info_font)
            x = (image.width - info_width) / 2
            draw.text((x, y), info, font=info_font, fill='black')
            y += 40

        return canvas

    def create_cover(self, title, other_info=None, output_path="output/cover.png", art_style=None, image_size=None):
        """Create a complete book cover with title and other information"""
        # Generate the cover illustration
        cover_image = self.generate_cover_image(title, art_style, image_size)
        if cover_image is None:
            raise ValueError("Failed to generate cover image")
        
        # Create a new white canvas (typical book cover proportions)
        canvas_width = 1200
        canvas_height = 1600
        canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
        draw = ImageDraw.Draw(canvas)
        
        # Resize and paste the illustration
        illustration_height = int(canvas_height * 0.8)  # Leave space for text
        resized_image = cover_image.resize((canvas_width, illustration_height))
        canvas.paste(resized_image, (0, 0))
        
        # Add text
        if other_info is None:
            other_info = []
        canvas = self.add_text_to_cover(canvas, title, other_info)
        
        # Add current year at the bottom
        year = str(datetime.now().year)
        year_width = draw.textlength(year, font=ImageFont.truetype("arial.ttf", 40))
        x = (canvas_width - year_width) / 2
        draw.text((x, canvas_height - 60), year, font=ImageFont.truetype("arial.ttf", 40), fill='black')
        
        # Save the final cover
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        canvas.save(output_path)
        return canvas
