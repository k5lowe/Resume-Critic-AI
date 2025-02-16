from pypdf import PdfReader
# import pdfplumber

path = r"C:\Users\kushi\OneDrive\Documents\University\11. Winter 2025\Coop\Kushini Lowe - Resume (Jan 14).pdf"

# path = r"path\to\resume"
reader = PdfReader(path)

# page = reader.pages[0]
# text = page.extract_text()
# print(text)

print(reader)






# def extract_text_from_pdf(pdf_path):
#     with pdfplumber.open(pdf_path) as pdf:
#         text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
#     return text

# resume_text = extract_text_from_pdf(path)
# print(resume_text)







