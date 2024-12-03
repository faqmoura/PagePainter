import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw, ImageFont
import os

class PagePainter:
    def __init__(self):
        """Initialize the PagePainter with the Stable Diffusion model"""
        # Initialize the model
        model_id = "CompVis/stable-diffusion-v1-4"
        
        # Force CPU mode for better compatibility
        self.device = "cpu"
        
        # Load the pipeline
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            safety_checker=None
        )
        
        self.pipe = self.pipe.to(self.device)
        
        # Enable basic memory optimizations
        self.pipe.enable_attention_slicing()
        self.pipe.enable_vae_slicing()
        
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
        
        # Generate the image with optimized settings for CPU
        with torch.inference_mode():
            image = self.pipe(
                prompt,
                num_inference_steps=15,  # Reduced for faster generation
                guidance_scale=7.5,
                height=image_size["height"],
                width=image_size["width"]
            ).images[0]
        
        return image
    
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
