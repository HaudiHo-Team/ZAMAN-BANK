import requests
from bs4 import BeautifulSoup
from fpdf import FPDF


url = 'https://www.zamanbank.kz/ru/islamic-finance/islamskie-finansy'

response = requests.get(url)
response.raise_for_status()


soup = BeautifulSoup(response.text, 'html.parser')


pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()


pdf.set_font("Arial", size=12, style='B')
pdf.cell(200, 10, txt="FAQ Парсинг данных с сайта Zaman Bank", ln=True, align="C")


pdf.set_font("Arial", size=12)


faq_section = soup.find_all('div', class_='py-6 border-b border-gray-300 last:border-0 last:pb-0')


for faq in faq_section:
    question = faq.find('div', class_='text-2xl font-semibold md:text-3xl md:leading-[36px]')
    if question:
        pdf.ln(10)
        pdf.set_font("Arial", size=12, style='B')
        pdf.multi_cell(0, 10, f"Вопрос: {question.get_text(strip=True)}")

    answer = faq.find('div', class_='_cie-faq w-full md:w-9/12')
    if answer:
        answer_text = answer.find('p')
        if answer_text:
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"Ответ: {answer_text.get_text(strip=True)}")

    pdf.ln(5)


pdf_output_path = "faq_parsing_output.pdf"
pdf.output(pdf_output_path)

print(f"PDF файл с результатами парсинга сохранен как {pdf_output_path}")