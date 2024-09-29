import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ParsedChatCompletion
from pydantic import BaseModel

from process_invoice_pdf import get_invoices

load_dotenv()

openai_api_client = OpenAI()

INVOICES_PROMPT = '''
You are a financial assistant that specialises in reading invoices from a food delivery app.
You will be provided with an invoice and your task is to extract the following information from the invoice: 

- Order number
- Order date 
- Restaurant name
- Order total

Answer in JSON list in the specified format.
---------
Here is one example showcasing the invoice and the result.

Example invoice
Order receipt
How would you rate the overall quality of your food experience?
Rate your order
Customer: Order:
Sold to: Nemanja Order number: y81k-hyk
Order date: 2024-01-12 10:18:29
Partner:
Name: Awesome Japan
Address: 23 Serangoon Central , #01-
63/64/65 NEX, 556083, Singapore
Item Qty Unit price Price
Japanese Rice 1 S$ 2.50 S$ 2.50
Chicken Teriyaki Don Bundle 1 S$ 13.00 S$ 13.00
- Coke 1 S$ 0.00 S$ 0.00
Spicy Miso Chicken Teppan 1 S$ 12.90 S$ 12.90
Subtotal S$ 28.40
Foodpanda delivery fee S$ 1.99
Platform fee S$ 0.40
Voucher -
Discount -
Order Total S$ 21.23
GST on foodpanda services S$ 0.19
Payment method:
Credit Card: S$ 21.23
Privacy | Terms and conditions
63 Robinson Road | Afroasia i-Mark Building #11-01 | Singapore 068894
© Delivery Hero (Singapore) Pte Ltd
GST No: 201209757Z

Expected example response in JSON:
{example_invoice}
--------

Extract the information from the following invoice.
'''

class Invoice(BaseModel):
    order_number: str
    order_date: str
    restaurant_name: str
    order_total: float


dummy_invoice = Invoice(order_number="y81k-hyk",
                        order_date="2024-01-12 10:18:29",
                        restaurant_name="Awesome Japan",
                        order_total=21.23)

invoices = get_invoices()

for invoice in invoices:
    extracted_invoice: ParsedChatCompletion[Invoice]  = openai_api_client.beta.chat.completions.parse(
        model=os.environ.get('CHAT_COMPLETION_MODEL'),
        response_format=Invoice,
        messages=[
            {"role": "system", "content": INVOICES_PROMPT.format(example_invoice=dummy_invoice.model_dump_json())},
            {
                "role": "user",
                "content": invoice
            }
        ]
    )

    print(extracted_invoice.choices[0].message.parsed.model_dump_json())