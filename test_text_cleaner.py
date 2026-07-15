"""
Test text_cleaner.py

Run:
python test_text_cleaner.py
"""

from rag.pdf_loader import extract_text_from_pdf
from rag.text_cleaner import clean_text

PDF_PATH = "data/sample_contracts/EMPLOYMENT-AGREEMENT.pdf"


def main():

    print("=" * 60)
    print("TESTING TEXT CLEANER")
    print("=" * 60)

    try:

        pdf_data = extract_text_from_pdf(PDF_PATH)

        raw_text = pdf_data["text"]

        cleaned_text = clean_text(raw_text)

        print(f"\nRaw Characters      : {len(raw_text)}")
        print(f"Cleaned Characters  : {len(cleaned_text)}")

        print("\nFirst 500 Characters (Cleaned)\n")
        print("-" * 60)
        print(cleaned_text[:500])
        print("-" * 60)

        print("\n✅ Text Cleaning Successful")

    except Exception as e:
        print("\n❌ ERROR")
        print(e)


if __name__ == "__main__":
    main()