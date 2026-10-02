import fitz
from docx import Document

def pdf_text(path):
    doc=fitz.open(path)
    txt=[]

    for page in doc:
        txt.append(page.get_text())

    doc.close()
    return "\n".join(txt).strip()

def docx_text(path):
    doc=Document(path)
    txt=[]

    for p in doc.paragraphs:
        if p.text.strip():
            txt.append(p.text.strip())

    return "\n".join(txt).strip()

def get_text(path):
    if path.lower().endswith(".pdf"):
        return pdf_text(path)

    if path.lower().endswith(".docx"):
        return docx_text(path)

    return ""