from fitz import *
from PIL import Image
import sys

DEFAULT_DPI = 72


def getDPI(needed):
    return needed / DEFAULT_DPI


def openPDFBytes(filename):
    pdf_file = fitz.open(filename)
    byte_arr = set()
    for page in pdf_file:
        pixmap = page.getPixmap(matrix=Matrix(getDPI(300), getDPI(300)))
        byte_arr.add(pixmap.tobytes())
    return byte_arr


def openPDF(filename):
    return fitz.open(filename)


def generatePDFName(name_samp, counter=1):
    name_samp = name_samp.split("/")
    main_part = name_samp[-1].split('.')
    main_part[0] = main_part[0] + f"_{str(counter)}"
    main_part = ".".join(main_part)
    name_samp[-1] = main_part
    name_samp = "/".join(name_samp)
    return name_samp


def savePDFtoPNG(newname, file):
    counter = 1
    for page in file:
        pix = page.getPixmap(matrix=Matrix(getDPI(300), getDPI(300)))
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        img.save(generatePDFName(newname, counter))
        counter += 1

