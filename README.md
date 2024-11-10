# Drawbook

Drawbook is a Python library that helps you create illustrated children's books using PowerPoint. It leverages AI to generate beautiful watercolor-style illustrations and formats them into a cohesive and visually appealing presentation.

## Features
- **AI-Generated Illustrations**: Automatically create watercolor illustrations based on the text you provide.
- **Book Quickstarter**: Generate an editable presentation (PowerPoint/Google Slides) that serves as a starting point - you can then change the layouts, images, and text to perfect your final design.
- **User-Friendly API**: Simple and intuitive Python API for creating books with custom titles, pages, and author details.

## Installation
To install Drawbook, use `pip`:

```bash
pip install drawbook
```

## Usage
Here’s how you can create an illustrated book using Drawbook:

```python
from drawbook import Book

book = Book(
    title="Mustafa's Trip To Mars",
    pages=[
        "Mustafa loves his silver cybertuck.\nOne day, his truck starts to glow, grow, and zoom up into the sky!",
        "Up, up, up goes Mustafa in his special truck.\nHe waves bye-bye to his house as it gets tiny down below.",
        "The stars look like tiny lights all around him.\nHis truck flies fast past the moon and the sun.",
        "Look! Mars is big and red like a giant ball.\nMustafa's truck lands softly on the red sand.",
        "Mustafa drives his truck on Mars and sees two small moons in the sky.\n\"This is fun!\" says Mustafa as he makes tracks in the red dirt.",
    ],
    author="Abubakar Abid"
)

book.illustrate()  # Generates illustrations for every page

book.export("Mustafas_Trip_To_Mars.pptx")
```

## Example Output
When you run the code above, Drawbook will generate a PowerPoint file (`Mustafas_Trip_To_Mars.pptx`) that contains:
- Text content formatted across multiple slides.
- AI-generated watercolor illustrations that match the content of each page.

## Customization Options
- **Title Page**: Customize the book’s cover with a unique title and author name.
- **Illustration Styles**: Choose between different AI styles for varied illustration aesthetics (coming soon).
- **Slide Layouts**: Configure the layout of text and images within the slides.

## Contributing
Contributions to Drawbook are welcome! If you have ideas for new features or improvements, feel free to submit an issue or pull request on the [GitHub repository](#).

## License
Drawbook is open-source software licensed under the [MIT License](LICENSE).
