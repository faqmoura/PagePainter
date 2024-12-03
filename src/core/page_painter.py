import os
from PIL import Image, ImageDraw, ImageFont
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from dotenv import load_dotenv
import io

class PagePainter:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv(override=True)
        
        # Get API key from environment variable and print it for debugging
        self.api_key = os.getenv("STABILITY_KEY")
        print(f"API Key loaded: {self.api_key}")
        
        if not self.api_key:
            raise ValueError("Please set STABILITY_KEY environment variable with your DreamStudio API key")
        
        # Initialize the stability client
        self.stability_api = client.StabilityInference(
            key=self.api_key,
            verbose=True,
        )
        
    def generate_illustration(self, description):
        """Generate an illustration based on the description"""
        # Add watercolor style to the prompt
        prompt = f"watercolor style illustration, children's book style, {description}"
        
        # Generate the image
        answers = self.stability_api.generate(
            prompt=prompt,
            seed=42,
            steps=20,
            cfg_scale=7.0,
            width=512,
            height=512,
            samples=1,
            sampler=generation.SAMPLER_K_DPMPP_2M
        )
        
        # Process the generated image
        for answer in answers:
            for artifact in answer.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    raise ValueError("Your request activated the API's safety filters")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    return img
        
        raise RuntimeError("Failed to generate image")
    
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
        canvas.save(output_path)
        return canvas

    def create_book_page(self, text, description, output_path):
        """Main method to create a book page"""
        # Generate the illustration
        illustration = self.generate_illustration(description)
        
        # Create and save the final page
        return self.create_page(text, illustration, output_path)
