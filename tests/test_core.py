from drawbook.core import Book
from pathlib import Path

def test_book_creation():
    book = Book()
    assert book.title == "Untitled Book"
    assert book.pages == []
    assert book.illustrations == []

def test_book_with_parameters():
    book = Book(
        title="My Book",
        pages=["Page 1", "Page 2"],
        illustrations=[None, False]
    )
    assert book.title == "My Book"
    assert len(book) == 2
    assert book.illustrations == [None, False]

def test_export():
    book = Book(
        title="Test Book",
        pages=["Page 1", "Page 2"],
        illustrations=[None, False]
    )
    book.export()
    # Note: We can't easily test the exact file location since it's temporary,
    # but we can verify the method runs without errors 