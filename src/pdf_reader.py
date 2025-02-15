import PyPDF2

class PDFReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_pdf(self):
        pdf_reader = PyPDF2.PdfReader(self.file_path)
        
        text = ""
        for page in range(0, len(pdf_reader.pages)):
            page_text = pdf_reader.pages[page].extract_text()
            text += page_text + "\n"
        return text

    def extract_text(self, raw_text):
        return raw_text.strip()