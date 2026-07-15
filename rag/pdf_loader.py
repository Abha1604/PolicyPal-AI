import fitz


def extract_text_from_pdf(pdf_path):
    """Extracts all text from a PDF.
    Parameters:
        pdf_path (str): Path of the PDF file.
    Returns:
        tuple:
            text (str)
            number_of_pages (int)
    """

    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    number_of_pages = len(document)

    document.close()

    return text, number_of_pages