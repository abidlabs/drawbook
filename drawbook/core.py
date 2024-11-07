"""
Core functionality for the drawbook library.
"""

from pathlib import Path
from typing import List
import tempfile
import io
import requests
from tqdm import tqdm
from PIL import Image
from huggingface_hub import HfApi
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN

class Book:
    """A class representing a children's book that can be exported to PowerPoint."""
    
    def __init__(
        self,
        title: str = "Untitled Book",
        pages: List[str] = None,
        illustrations: List[str | None | bool] = None
    ):
        """
        Initialize a new Book.
        
        Args:
            title: The book's title
            pages: List of strings containing text for each page
            illustrations: List of illustration paths or placeholders
                         (str for path, None for pending, False for no illustration)
        """
        self.title = title
        self.pages = pages or []
        self.illustrations = illustrations or []
        
        # Ensure illustrations list matches pages length
        while len(self.illustrations) < len(self.pages):
            self.illustrations.append(None)
    
    def export(self, filename: str | Path | None = None) -> None:
        """
        Export the book to a PowerPoint file.
        
        Args:
            filename: Optional path where to save the file. If None, creates in temp directory.
        """
        if filename is None:
            # Create temp file with .pptx extension
            temp_file = tempfile.NamedTemporaryFile(suffix='.pptx', delete=False)
            output_path = Path(temp_file.name)
            temp_file.close()
        else:
            # Convert to Path object and resolve to absolute path
            output_path = Path(filename).resolve()
            # Ensure parent directories exist
            output_path.parent.mkdir(parents=True, exist_ok=True)

        prs = Presentation()
        
        # Add title slide
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)
        title = slide.shapes.title
        title.text = self.title
        # Add font styling to title
        title.text_frame.paragraphs[0].font.name = "Noteworthy"
        
        # Add content slides
        content_slide_layout = prs.slide_layouts[5]  # Blank layout
        
        for page_num, (text, illustration) in enumerate(zip(self.pages, self.illustrations)):
            slide = prs.slides.add_slide(content_slide_layout)
            
            # Add text
            txBox = slide.shapes.add_textbox(
                Inches(0.5), Inches(0.5),
                Inches(9), Inches(1)
            )
            tf = txBox.text_frame
            
            # Special formatting for first page
            if page_num == 0 and text:
                # Split first character from rest of text
                first_char = text[0]
                rest_of_text = text[1:]
                
                p = tf.paragraphs[0]
                run = p.add_run()
                run.text = first_char
                run.font.size = Inches(0.3)  # Make first letter larger
                run.font.name = "Geneva"
                
                run = p.add_run()
                run.text = rest_of_text
                run.font.size = Inches(0.25)  # Regular text size
                run.font.name = "Geneva"
            else:
                tf.text = text
                tf.paragraphs[0].font.name = "Geneva"
                tf.paragraphs[0].font.size = Inches(0.25)  # Match size with first page
            
            # Add illustration if available
            if isinstance(illustration, str):
                try:
                    slide.shapes.add_picture(
                        illustration,
                        Inches(1), Inches(2),
                        Inches(8), Inches(4)
                    )
                except Exception as e:
                    print(f"Warning: Could not add illustration on page {page_num + 1}: {e}")
            
            # Add page number at bottom center
            page_number = page_num + 1  # Add 1 since page_num is 0-based
            page_num_box = slide.shapes.add_textbox(
                Inches(0), Inches(6.5),  # Y position near bottom of slide
                Inches(10), Inches(0.5)  # Full width of slide for centering
            )
            page_num_frame = page_num_box.text_frame
            page_num_frame.text = str(page_number)
            page_num_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
            page_num_frame.paragraphs[0].font.name = "Geneva"
            page_num_frame.paragraphs[0].font.size = Inches(0.15)  # Slightly smaller than main text
        
        # Save the presentation
        prs.save(str(output_path))
        print(f"Book exported to: {output_path.absolute()}")
    
    def __len__(self) -> int:
        """Return the number of pages in the book."""
        return len(self.pages)

    def illustrate(self, save_dir: str | Path | None = None) -> None:
        """
        Generate illustrations for all pages using the Hugging Face Inference API.
        
        Args:
            save_dir: Optional directory to save the generated images. 
                     If None, creates a temporary directory.
        """
        # Get HF token
        hf_api = HfApi()
        token = hf_api.get_token()
        if not token:
            raise ValueError("No Hugging Face token found. Please login using `huggingface-cli login`")

        API_URL = "https://api-inference.huggingface.co/models/SebastianBodza/Flux_Aquarell_Watercolor_v2"
        headers = {"Authorization": f"Bearer {token}"}

        # Create save directory if provided
        if save_dir:
            save_dir = Path(save_dir)
            save_dir.mkdir(parents=True, exist_ok=True)
        else:
            save_dir = Path(tempfile.mkdtemp())

        print("Generating illustrations... This could take a few minutes.")
        
        # Generate illustrations for each page
        for i, (text, current_illust) in enumerate(tqdm(zip(self.pages, self.illustrations), total=len(self.pages))):
            # Skip if illustration already exists
            if isinstance(current_illust, str):
                continue
                
            # Skip if illustration is explicitly disabled
            if current_illust is False:
                continue
                
            try:
                # Query the API
                response = requests.post(API_URL, headers=headers, json={"inputs": text})
                if response.status_code != 200:
                    print(f"Warning: Failed to generate illustration for page {i+1}: {response.text}")
                    continue
                    
                # Save the image
                image = Image.open(io.BytesIO(response.content))
                image_path = save_dir / f"page_{i+1}.png"
                image.save(image_path)
                
                # Update the illustrations list
                self.illustrations[i] = str(image_path)
                
            except Exception as e:
                print(f"Warning: Error generating illustration for page {i+1}: {e}")
                continue

        print(f"Illustrations saved to: {save_dir}")