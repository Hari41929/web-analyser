import threading
from analyzer import extract_from_url
from pdf_generator import create_pdf

def process_url(url, index):
    print(f"Processing {url.strip()}")
    data = extract_from_url(url.strip())
    if data:
        filename = f"output_{index + 1}.pdf"
        create_pdf(data, filename)
        print(f"✅ PDF created → {filename}")
    else:
        print(f"❌ Skipped {url}")

def main():
    urls = input("Enter URLs (comma-separated): ").split(',')
    threads = [threading.Thread(target=process_url, args=(url, idx)) for idx, url in enumerate(urls)]

    for t in threads: t.start()
    for t in threads: t.join()

    print("🎉 All PDFs generated.")

if __name__ == "__main__":
    main()