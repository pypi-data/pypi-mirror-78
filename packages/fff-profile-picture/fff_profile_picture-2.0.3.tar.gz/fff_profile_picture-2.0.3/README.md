# FFF Profile Picture Lib
## What is it?
A library to generate profile pictures

## Example
```python
from fff_profile_picture import Generator
from PIL import Image

generator = Generator(Image.open("original.JPG"), Image.open("overlay.png"))
result = generator.process()
result.save("generated.png")
```

## Docs

https://fff-bots.gitlab.io/fff-profile-picture-python/

