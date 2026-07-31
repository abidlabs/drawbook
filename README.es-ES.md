

# Drawbook

`drawbook` es una biblioteca de Python que te ayuda a crear libros ilustrados para niños usando IA. Aprovecha modelos de IA de generación de imágenes para crear ilustraciones estilo acuarela que corresponden al texto que has escrito y luego las exporta a un archivo de PowerPoint / Slides que puedes editar más adelante.

![](https://github.com/abidlabs/drawbook/blob/main/assets/0.png?raw=true)

## Características
- **Ilustraciones generadas por IA**: Crea automáticamente ilustraciones estilo acuarela basadas en el texto que proporciones.
- **Crea ilustraciones programáticamente o con una interfaz de usuario amigable**: Genera ilustraciones con una sola línea de Python: `book.illustrate()`, o abre una interfaz de Gradio en tu navegador: `book.preview()`, para tener un control más detallado sobre las ilustraciones.
- **Comienza rápido, perfecciona después**: Exporta tus ilustraciones a una presentación (PowerPoint/Google Slides) que sirve como punto de partida; luego puedes cambiar los diseños, imágenes y texto para perfeccionar tu diseño final.
- **Gratis**: Este proyecto utiliza la API de Inferencia gratuita de Hugging Face para generar ilustraciones. Recomendamos encarecidamente tener una cuenta Hugging Face Pro para evitar límites de velocidad.

## Requisitos previos
* Python 3.10+
* Membresía Hugging Face Pro (muy recomendada, ya que este proyecto utiliza la API de Inferencia gratuita de Hugging Face)

## Instalación
Para instalar Drawbook, utiliza `pip`:

```bash
pip install drawbook
```

## Uso
Así es como puedes crear un libro ilustrado usando Drawbook en unas pocas líneas de Python:

```python
from drawbook import Book

book = Book(title="Mustafa's Trip to Mars", pages=[
    "One day, Mustafa climbs into the attic and finds a white spacesuit.",
    "He puts on the spacesuit and the spacesuit starts to glow!",
    "Mustafa starts to float up into the air in his spacesuit. He waves bye-bye to his house as it gets tiny down below.",
    "The stars look like tiny lights all around him. His spacesuit flies fast past the moon and the sun.",
    "Mustafa lands on Mars. The landing makes a big crater in the Martian surface.",
    "Mustafa explores Mars in his spacesuit. He meets a Martian and waves hello to him.",
    "Mustafa and the Martian play with toys on Mars. They have a great time together!",
], author="Abubakar Abid")

book.illustrate()  # Generates illustrations for every page

book.export("Mustafas_Trip_To_Mars.pptx")
```

Al ejecutar el código anterior, Drawbook generará un archivo de PowerPoint (`Mustafas_Trip_To_Mars.pptx`) que contiene:
- Contenido de texto formateado en varias diapositivas.
- Ilustraciones estilo acuarela generadas por IA que coinciden con el contenido de cada página.

## Vista previa y refinamiento

Si deseas regenerar las ilustraciones de cualquier página específica, simplemente ejecuta:

```
book.preview()
```

Esto abrirá una [demo de Gradio](https://gradio.dev/) que te permite ver el prompt utilizado para crear cada ilustración. Puedes editar el prompt y seguir regenerando imágenes hasta tener una gran serie de ilustraciones para tu libro. Una vez que hayas terminado, simplemente haz clic en "Export" y luego en "Download" para obtener tus diapositivas exportadas.

![](https://github.com/abidlabs/drawbook/blob/main/assets/demo.png?raw=true)

## Contribuir
¡Las contribuciones a `drawbook` son bienvenidas! Si tienes ideas para nuevas características o mejoras, no dudes en enviar un issue o pull request en el [repositorio de GitHub](#).

## Licencia
Drawbook es software de código abierto licenciado bajo la [Licencia MIT](LICENSE).

## Versión
La versión actual se encuentra en `version.txt` en el directorio raíz, o se puede acceder programáticamente mediante:
