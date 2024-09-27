import pdfplumber


def get_invoices():

    for invoice_id in range(1, 6):
        print(invoice_id)
        with pdfplumber.open(f"./invoices/invoice-{invoice_id}.pdf") as invoice_pdf:
            for page in invoice_pdf.pages:
                print(page.extract_text())


get_invoices()