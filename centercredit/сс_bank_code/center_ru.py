import camelot
import pandas as pd
import json
import re
import PyPDF2

pdf_file_path = "cc_bank_pdfs/center_ru.pdf"
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
fio_re = r'\d{2}\.\d{2}\.\d{4}\s-\s\d{2}\.\d{2}.\d{4}\n(\D+?)\sИИН'
fio = re.search(fio_re, pdf_text).group(1)
fio = ' '.join(fio.split())
print(fio)

# ИИН
iin_re = r'ИИН:\s(\d+)'
iin = re.search(iin_re, pdf_text).group(0)
iin = ' '.join(iin.split())
print(iin)

# Инфа об счете 
# Валюта
curr_re = r'Валюта\s+(\w+)'
curr = re.search(curr_re, pdf_text).group(0)
curr = ' '.join(curr.split())
print(curr)
# Карта
card_re = r'Карта\s+\d+\*{6}\d+'
card = re.search(card_re, pdf_text).group(0)
card = ' '.join(card.split())
print(card)
# Счет
acc_re = r'Тип\s+(\w+)\s+(\w+)'
acc = re.search(acc_re, pdf_text).group(0)
acc = ' '.join(acc.split())
print(acc)
# Период
per_re = r'Период\s+\d{2}\.\d{2}\.\d{4}\s-\s\d{2}\.\d{2}.\d{4}'
per = re.search(per_re, pdf_text).group(0)
per = ' '.join(per.split())
print(per)

header_data = {
    "fio": fio,
    "iin": iin,
    "currency": curr,
    "card": card,
    "card_number": acc,
    "period": per
}

data = []

pdf_text = pdf_text.replace(chr(9), ' ')  # заменяем табы на пробелы
pdf_text = pdf_text.replace('\n', ' ')  # заменяем табы на пробелы

pos_start = pdf_text.find("Cashback, KZT")
pos_start += len("Cashback, KZT")
pdf_text = pdf_text[pos_start:]

# print("->", pdf_text, "<-")

row_re = r'(\d\d\.\d\d\.20\d\d +\d\d:\d\d:\d\d) +(\d\d\.\d\d\.20\d\d)(.*?)Плательщик:(.*?)(\-?[\d ]+,\d\d)'

rows = re.findall(row_re, pdf_text)
for row in rows:
    result = {
        "date_operation": row[0],
        "date_show_account": row[1],
        "details": row[2],
        "payer": row[3],
        "amount": row[4],
    }
    data.append(result)
    print(result)

centercredit_data = {
    "header_data": header_data,
    "transactions": data
}
with open('cc_bank_jsons/ru.json', 'w', encoding='utf-8') as json_file:
    json.dump(centercredit_data, json_file, ensure_ascii=False, indent=4)