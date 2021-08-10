from fitz import *
from PIL import Image
import sys, os, zipfile

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


def savePDFtoPNG(newname, file, dpi=300, arc=None):
    counter = 1
    for page in file:
        pix = page.getPixmap(matrix=Matrix(getDPI(dpi), getDPI(dpi)))
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        img.save(generatePDFName(newname, counter))
        if arc is not None:
            arc_name = generatePDFName(newname, counter).split("/")[-1]
            arc.write(arc_name, arcname=arc_name)
        counter += 1


def convertPDF(f, meta):
    fname = f.split('/')[-1].split('.')[0]
    arc = None
    if meta["do_fold"]:
        os.mkdir(os.path.join(meta["dest"], fname))
        newname = meta["dest"] + "/" + fname + '/' + fname + "." + meta["ext"]
    else:
        newname = meta["dest"] + "/" + fname + "." + meta["ext"]

    if meta["do_arc"]:
        arc = zipfile.ZipFile(meta["dest"] + '/' + fname + "_arc.zip", "w")
        print(arc.filename)

    savePDFtoPNG(newname, openPDF(f), meta["dpi"], arc=arc)

    if meta["do_arc"]:
        arc.close()