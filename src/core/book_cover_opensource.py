import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

class BookCover:
    def __init__(self):
        """Initialize the BookCover with the Stable Diffusion model"""
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
        
        # Generate the image
        with torch.inference_mode():
            image = self.pipe(
                prompt,
                num_inference_steps=15,
                guidance_scale=7.5,
                height=image_size["height"],
                width=image_size["width"]
            ).images[0]
        
        return image
    
    def create_cover(self, title, other_info=None, output_path="output/cover.png", art_style=None, image_size=None):
        """Create a complete book cover with title and other information"""
        # Generate the cover illustration
        cover_image = self.generate_cover_image(title, art_style, image_size)
        
        # Create a new white canvas (typical book cover proportions)
        canvas_width = 1200
        canvas_height = 1800
        canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
        
        # Resize and paste the illustration
        illustration_height = int(canvas_height * 0.8)  # Leave space for text
        resized_image = cover_image.resize((canvas_width, illustration_height))
        canvas.paste(resized_image, (0, 0))
        
        # Add text
        draw = ImageDraw.Draw(canvas)
        
        # Try to use different fonts for title and other text
        try:
            title_font = ImageFont.truetype("arial.ttf", 120)  # Larger size for title
            info_font = ImageFont.truetype("arial.ttf", 48)    # Smaller size for other info
        except:
            title_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
        
        # Add title at the top
        # Word wrap for title
        words = title.split()
        lines = []
        current_line = []
        margin = 60
        
        for word in words:
            current_line.append(word)
            text_width = draw.textlength(' '.join(current_line), font=title_font)
            if text_width > canvas_width - 2 * margin:
                if len(current_line) == 1:
                    lines.append(current_line[0])
                    current_line = []
                else:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw title with shadow effect
        title_y = 50  # Top margin
        for line in lines:
            text_width = draw.textlength(line, font=title_font)
            x = (canvas_width - text_width) / 2
            
            # Draw shadow
            shadow_offset = 4
            draw.text((x + shadow_offset, title_y + shadow_offset), line, 
                     font=title_font, fill='grey')
            # Draw text
            draw.text((x, title_y), line, font=title_font, fill='black')
            title_y += int(title_font.size * 1.2)  # Move down for next line
        
        # Add other info at the bottom
        if other_info:
            info_y = canvas_height - 200  # Bottom margin
            for info in other_info:
                text_width = draw.textlength(info, font=info_font)
                x = (canvas_width - text_width) / 2
                draw.text((x, info_y), info, font=info_font, fill='black')
                info_y += int(info_font.size * 1.2)
        
        # Add current year at the bottom
        year = str(datetime.now().year)
        year_width = draw.textlength(year, font=info_font)
        x = (canvas_width - year_width) / 2
        draw.text((x, canvas_height - 80), year, font=info_font, fill='black')
        
        # Save the final cover
        canvas.save(output_path)
        return canvas

def main():
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Initialize BookCover
    print("Initializing BookCover (this may take a few moments to download the model)...")
    cover_maker = BookCover()
    
    # Example inputs
    title = "The Magical Rainbow Rabbit"
    other_info = [
        "Written by Jane Smith",
        "Illustrated by PagePainter AI"
    ]
    
    # Generate the cover
    print("Generating book cover...")
    output_path = "output/book_cover.png"
    cover_maker.create_cover(title, other_info, output_path)
    print(f"Book cover created successfully! Check {output_path}")

if __name__ == "__main__":
    main()
