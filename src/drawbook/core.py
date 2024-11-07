"""
Core functionality for the drawbook library.
"""

class Canvas:
    def __init__(self, width: int, height: int):
        """
        Initialize a new canvas with given dimensions.
        
        Args:
            width (int): Width of the canvas
            height (int): Height of the canvas
        """
        self.width = width
        self.height = height
        self.pixels = [[None for _ in range(width)] for _ in range(height)]
    
    def clear(self):
        """Clear the canvas."""
        self.pixels = [[None for _ in range(self.width)] for _ in range(self.height)] 