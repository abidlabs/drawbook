from drawbook.core import Canvas

def test_canvas_initialization():
    canvas = Canvas(10, 10)
    assert canvas.width == 10
    assert canvas.height == 10
    assert len(canvas.pixels) == 10
    assert len(canvas.pixels[0]) == 10

def test_canvas_clear():
    canvas = Canvas(5, 5)
    canvas.pixels[0][0] = "test"
    canvas.clear()
    assert canvas.pixels[0][0] is None 