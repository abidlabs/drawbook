# Drawbook

`drawbook` is a Python library that helps you create illustrated children's books using AI. It leverages image generation AI models to generate watercolor-style illustrations corresponding to text that you have written and then exports them to a PowerPoint / Slides file that you can further edit.

## Features
- **AI-Generated Illustrations**: Automatically create watercolor illustrations based on the text you provide.
- **Create Illustrations Programmatically or with a User-Firendly UI**: Create illustrations with a single of Python -- `.illustrate()` --, or a open up a Gradio UI in your browser -- `.preview()` -- to have more fine-grained control over the illustrations.
- **Start Quickly, Refine Later**: Export your illustrations a presentation (PowerPoint/Google Slides) that serves as a starting point - you can then change the layouts, images, and text to perfect your final design.


## Installation
To install Drawbook, use `pip`:

```bash
pip install drawbook
```

## Usage
Here’s how you can create an illustrated book using Drawbook in a few lines of Python:

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

When you run the code above, Drawbook will generate a PowerPoint file (`Mustafas_Trip_To_Mars.pptx`) that contains:
- Text content formatted across multiple slides.
- AI-generated watercolor illustrations that match the content of each page.

## Preview & Refine



## Contributing
Contributions to Drawbook are welcome! If you have ideas for new features or improvements, feel free to submit an issue or pull request on the [GitHub repository](#).

## License
Drawbook is open-source software licensed under the [MIT License](LICENSE).
