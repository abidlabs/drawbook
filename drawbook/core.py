"""
Core functionality for the drawbook library.
"""

from pathlib import Path
from typing import List
import tempfile
from pptx import Presentation
from pptx.util import Inches

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
    
    def export(self) -> None:
        """
        Export the book to a PowerPoint file in a temporary location and print the path.
        """
        # Create temp file with .pptx extension
        temp_file = tempfile.NamedTemporaryFile(suffix='.pptx', delete=False)
        output_path = Path(temp_file.name)
        temp_file.close()

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
        
        # Save the presentation
        prs.save(str(output_path))
        print(f"Book exported to: {output_path.absolute()}")
    
    def __len__(self) -> int:
        """Return the number of pages in the book."""
        return len(self.pages)