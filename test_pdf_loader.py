from rag.pdf_loader import extract_text_from_pdf


pdf_path = "data/sample_contracts/COE-Sample.pdf"
# Change this if your filename is different.


text, pages = extract_text_from_pdf(pdf_path)

print("\n" + "=" * 60)
print("PDF LOADED SUCCESSFULLY")
print("=" * 60)

print(f"Pages      : {pages}")
print(f"Characters : {len(text)}")

print("\nFirst 500 characters:\n")
print(text[:500])