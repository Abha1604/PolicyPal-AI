from rag.pdf_loader import extract_text_from_pdf
from rag.text_cleaner import clean_text
pdf_path = "data/sample_contracts/COE-Sample.pdf"
raw_text, pages = extract_text_from_pdf(pdf_path)
cleaned_text = clean_text(raw_text)
print("=" * 60)
print("RAW TEXT")
print("=" * 60)
print(raw_text[:500])
print("\n")
print("=" * 60)
print("CLEANED TEXT")
print("=" * 60)
print(cleaned_text[:500])
