import PyPDF2
import re
import json

pdf_file_path = "centercredit/center_eng.pdf"
def extract_text_from_pdf(pdf_file_path):
    text = ""
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()

    return text 

if pdf_file_path != 0:
    pdf_text = extract_text_from_pdf(pdf_file_path)
else:
    print("file is empty")

# Поиск ФИО
fio_re = r'\d{2}\.\d{2}\.\d{4}\s-\s\d{2}\.\d{2}.\d{4}\n(\D+?)\sIIN'
fio = re.search(fio_re, pdf_text) 
fio = fio.group(1)
fio = ' '.join(fio.split())
print(fio)

# ИИН
iin_re = r'IIN:\s(\d+)'
iin = re.search(iin_re, pdf_text)
iin = iin.group(0)
iin = ' '.join(iin.split())
print(iin)
