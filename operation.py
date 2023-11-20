from dataclasses import dataclass
from decimal import Decimal
import re
import datetime

import PyPDF2

@dataclass
class Operation:
    date: datetime.datetime
    amount: Decimal
    operation: str
    details: str

    @classmethod
    def parse(cls, a: str) -> "Operation":
        result = re.search(r'(\d\d)\.(\d\d)\.(\d\d) (.) (\d[\d\s]*),00 ₸ *(\w+) * (\w+)', a)
        if result:
            day = int(result.group(1))
            month = int(result.group(2))
            year = int(result.group(3))
            plus_minus = result.group(4)
            amount_str = result.group(5).replace(" ", "")  
            amount = Decimal(amount_str)  
            if plus_minus == "-":
                amount = -amount
            operation = result.group(6)
            details = result.group(7)
            return cls(
                date=datetime.datetime(year=2000+year, month=month, day=day),
                amount=amount,
                operation=operation,
                details=details,
            )
        else:
            return None
        
    def to_json(self) -> dict:
        formatted_date = self.date.strftime("%d-%m-%Y")
        return {
            "date": formatted_date,
            "amount": str(self.amount),
            "operation": str(self.operation),
            "details": str(self.details),
        }

pdf_file_path = "list1.pdf"
def extract_text_from_pdf(pdf_file_path):
    text = ""
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()

    return text 

pdf_text = extract_text_from_pdf(pdf_file_path)
transacs = r'\d{2}\.\d{2}\.\d{2}\s[+-]?\s[\d\s,]+\s[^\n]+'
res_transacs = re.findall(transacs, pdf_text)

# Пройдитесь по каждой строке и примените код для структурирования таблицы
transactions = [Operation.parse(row) for row in res_transacs if Operation.parse(row)]
for transaction in transactions:
    print(transaction.to_json())