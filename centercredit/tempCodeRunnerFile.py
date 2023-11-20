import camelot
import pandas as pd
import json
import re
import PyPDF2

pdf_file_path = "centercredit/center_ru.pdf"
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
    "ФИО": fio,
    "ИИН": iin,
    "Валюта": curr,
    "Карта": card,
    "Счет": acc,
    "Период": per
}

tables = camelot.read_pdf(pdf_file_path, flavor='stream', pages='all')

# заменяем символы на пробелы
for table in tables:
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            table.df.iloc[i, j] = table.df.iloc[i, j].replace('\t', ' ')
            table.df.iloc[i, j] = table.df.iloc[i, j].replace('\n', ' ')

import re

def extract_operations(description):
    operation_pattern = r'(?<!\d)\d{2}\.\d{2}\.\d{4}[\s\S]+?(?=\d{2}\.\d{2}\.\d{4}|\Z)'
    operations = re.findall(operation_pattern, description)
    return [operation.strip() for operation in operations]

# Прочитать таблицы и создать список словарей для каждой операции
data = []
for table in tables:
    for i in range(5, table.df.shape[0]):
        row = table.df.iloc[i]

        if row.str.strip().replace('', pd.NA).dropna().empty:
            continue

        operations = extract_operations(row[2])

        print(operations)

        entry = {
            "Дата операции": row[0],
            "Дата отражения на счете": row[1],
            "Детали": operations,
            "Сумма в валюте": row[3] if len(row) > 3 else None,
            "Сумма в KZT": row[4] if len(row) > 4 else None,
            "Комиссия": row[5] if len(row) > 5 else None,
            "Cashback": row[6] if len(row) > 6 else None
        }
        data.append(entry)

# Создать DataFrame и записать его в JSON
df = pd.DataFrame(data)
transactions = df.dropna()

centercredit_data = {
    "header_data": header_data,
    "transactions": transactions.to_dict(orient='records')
}
with open('centercredit_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(centercredit_data, json_file, ensure_ascii=False, indent=4)










