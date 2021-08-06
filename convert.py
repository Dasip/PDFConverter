from fitz import *
from PIL import Image


pdf = "Agro.pdf"
img_name = "IMG2.jpg"
img_name2 = "IMG3.jpg"
comp = "zip"

pdf_doc = fitz.open(pdf)
zoom = 1
mat = Matrix(zoom, zoom)

image_list = []
for page in pdf_doc:
    pix = page.getPixmap(matrix=Matrix(300/72, 300/72))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    image_list.append(img)
    break

image_list[0].save(img_name)
