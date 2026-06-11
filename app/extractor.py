import fitz  # PyMuPDF
# pyrefly: ignore [missing-import]
from docx import Document
import io

class TranscriptExtractor:
    @staticmethod
    def extract_from_text(text: str) -> str:
        return text

    @staticmethod
    def extract_from_txt(txt_bytes: bytes) -> str:
        return txt_bytes.decode("utf-8")

    @staticmethod
    def extract_from_pdf(pdf_bytes: bytes) -> str:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = []
        for page in doc:
            text.append(page.get_text())
        return "\n".join(text)

    @staticmethod
    def extract_from_docx(docx_bytes: bytes) -> str:
        doc = Document(io.BytesIO(docx_bytes))
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return "\n".join(text)
