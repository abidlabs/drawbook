"""
Core functionality for the drawbook library.
"""

from pathlib import Path
from typing import List, Literal
import tempfile
import io
import requests
import warnings
from tqdm import tqdm
from PIL import Image
import huggingface_hub
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_PATTERN

class Book:
    """A class representing a children's book that can be exported to PowerPoint."""
    
    def __init__(
        self,
        title: str = "Untitled Book",
        pages: List[str] = None,
        title_illustration: str | Literal[False] | None = None,
        illustrations: List[str | None | Literal[False]] = None,
        lora: str = "SebastianBodza/Flux_Aquarell_Watercolor_v2",
        author: str | None = None
    ):
        """
        Initialize a new Book.
        
        Args:
            title: The book's title
            pages: List of strings containing text for each page
            illustrations: List of illustration paths or placeholders
                         (str for path, None for pending, False for no illustration)
            lora: The LoRA model on Hugging Face to use for illustrations
            author: The book's author name
        """
        self.title = title
        self.pages = pages or []
        self.illustrations = illustrations or []
        self.lora = lora
        self.title_illustration = title_illustration
        self.author = author
        
        # Ensure illustrations list matches pages length
        while len(self.illustrations) < len(self.pages):
            self.illustrations.append(None)

    def _get_prompt(self, text: str) -> str:
        """Get the prompt for the given text using the LoRA model."""
        if self.lora == "SebastianBodza/Flux_Aquarell_Watercolor_v2":
            return f"A AQUACOLTOK watercolor painting to illustrate the following text: {text}"
        else:
            return f"An illustration of the following text: {text}"
    
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
        
        # Add diagonal striped border at the top
        border = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0),
            Inches(10), Inches(0.5)
        )
        border.fill.patterned()
        border.fill.pattern = MSO_PATTERN.DIAGONAL_BRICK
        border.fill.fore_color.rgb = RGBColor(128, 0, 0)  # Maroon
        border.fill.back_color.rgb = RGBColor(255, 255, 255)  # White
        
        # Add title at the top
        title = slide.shapes.title
        title.top = Inches(0.7)  # Position below border
        title.text = self.title
        title.text_frame.paragraphs[0].font.name = "Noteworthy"
        title.text_frame.paragraphs[0].font.color.rgb = RGBColor(128, 0, 0)  # Maroon
        
        # Add title illustration if available
        if isinstance(self.title_illustration, str):
            try:
                slide.shapes.add_picture(
                    self.title_illustration,
                    Inches(2), Inches(2.5),  # Centered horizontally, positioned below title
                    Inches(6), Inches(6)     # Square dimensions
                )
            except Exception as e:
                print(f"Warning: Could not add title illustration: {e}")
        
        # Add author if available
        if self.author is not None:
            author_box = slide.shapes.add_textbox(
                Inches(0), Inches(8.5),  # Position at bottom
                Inches(10), Inches(0.5)
            )
            author_frame = author_box.text_frame
            author_frame.text = f"Written by {self.author}"
            author_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
            author_frame.paragraphs[0].font.name = "Geneva"
            author_frame.paragraphs[0].font.size = Inches(0.2)
        
        # Add content slides
        content_slide_layout = prs.slide_layouts[5]  # Blank layout
        
        for page_num, (text, illustration) in enumerate(zip(self.pages, self.illustrations)):
            slide = prs.slides.add_slide(content_slide_layout)
            
            # Determine if text should be above or below illustration
            text_on_top = page_num % 2 == 0
            text_y = Inches(0.5) if text_on_top else Inches(4.5)
            illustration_y = Inches(2) if text_on_top else Inches(0.5)
            
            # Add text with center alignment
            txBox = slide.shapes.add_textbox(
                Inches(0.5), text_y,
                Inches(9), Inches(1)
            )
            tf = txBox.text_frame
            tf.word_wrap = True
            
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
                p.alignment = PP_ALIGN.CENTER  # Center align the first paragraph
            else:
                tf.text = text
                tf.paragraphs[0].font.name = "Geneva"
                tf.paragraphs[0].font.size = Inches(0.25)
                tf.paragraphs[0].alignment = PP_ALIGN.CENTER  # Center align the text
            
            # Add illustration if available
            if isinstance(illustration, str):
                try:
                    slide.shapes.add_picture(
                        illustration,
                        Inches(1), illustration_y,
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
        token = huggingface_hub.get_token()
        if not token:
            warnings.warn("No Hugging Face token found. Please login using `huggingface-cli login` or set the HF_TOKEN environment variable. Otherwise, you may be rate limited.")

        API_URL = f"https://api-inference.huggingface.co/models/{self.lora}"
        headers = {"Authorization": f"Bearer {token}"}

        # Create save directory if provided
        if save_dir:
            save_dir = Path(save_dir)
            save_dir.mkdir(parents=True, exist_ok=True)
        else:
            save_dir = Path(tempfile.mkdtemp())

        print("Generating illustrations... This could take a few minutes.")

        # Create a list of tasks for the progress bar
        tasks = []
        if self.title_illustration is None:
            tasks.append(("title", self.title, None))
        tasks.extend((f"page_{i+1}", text, current_illust) 
                     for i, (text, current_illust) in enumerate(zip(self.pages, self.illustrations)))

        for task_name, text, current_illust in tqdm(tasks, desc="Generating illustrations"):
            # Skip if illustration already exists or is explicitly disabled
            if isinstance(current_illust, str) or current_illust is False:
                continue
                
            try:
                # Query the API
                prompt = self._get_prompt(text)
                response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
                if response.status_code != 200:
                    print(f"Warning: Failed to generate illustration for {task_name}: {response.text}")
                    continue
                    
                # Save the image
                image = Image.open(io.BytesIO(response.content))
                image_path = save_dir / f"{task_name}.png"
                image.save(image_path)
                
                # Update the appropriate illustration reference
                if task_name == "title":
                    self.title_illustration = str(image_path)
                else:
                    page_num = int(task_name.split('_')[1]) - 1
                    self.illustrations[page_num] = str(image_path)
                    
            except Exception as e:
                print(f"Warning: Error generating illustration for {task_name}: {e}")
                continue

        print(f"Illustrations saved to: {save_dir}")