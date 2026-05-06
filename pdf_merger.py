from pypdf import PdfWriter

merger = PdfWriter()

for pdf in ["questions.pdf", "OOPS Important Interview Questions.pdf"]:
    merger.append(pdf)

merger.write("merged_pdf.pdf")