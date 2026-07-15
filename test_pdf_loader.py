"""
Test pdf_loader.py

Run:
python test_pdf_loader.py
"""

from rag.pdf_loader import extract_text_from_pdf

# Change filename if needed
PDF_PATH = "data/sample_contracts/EMPLOYMENT-AGREEMENT.pdf"


def main():

    print("=" * 60)
    print("TESTING PDF LOADER")
    print("=" * 60)

    try:

        pdf_data = extract_text_from_pdf(PDF_PATH)

        print("\n✅ PDF Loaded Successfully\n")

        print(f"Filename      : {pdf_data['filename']}")
        print(f"Pages         : {pdf_data['num_pages']}")
        print(f"Characters    : {len(pdf_data['text'])}")

        print("\nFirst 500 Characters\n")
        print("-" * 60)
        print(pdf_data["text"][:500])
        print("-" * 60)

    except Exception as e:
        print("\n❌ ERROR")
        print(e)


if __name__ == "__main__":
    main()