from PyPDF2 import PdfFileReader, PdfFileWriter

pdf_doc = "passport_other.pdf"
pdf = PdfFileReader(pdf_doc)
writer = PdfFileWriter()
page = pdf.getPage(2)
writer.addPage(page)
with open("passport{}.pdf".format(str(3)), "wb") as out:
    writer.write(out)
