import pdfplumber


def get_invoices() -> list[str]:

    invoices = []
    for invoice_id in range(1, 6):

        with pdfplumber.open(f"./invoices/invoice-{invoice_id}.pdf") as invoice_pdf:
            invoice = ""
            for page in invoice_pdf.pages:
                invoice += page.extract_text()

            invoices.append(invoice)
    return invoices