import os
import pandas as pd

# Tự động kiểm tra / cài đặt thư viện đọc PDF nếu cần
try:
    import pypdf
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "pypdf", "pandas", "openpyxl"])
    import pypdf

# Tạo thư mục lưu trữ dữ liệu thô
os.makedirs("research/data", exist_ok=True)


def process_cisco_pdf(pdf_path, output_csv):
    if not os.path.exists(pdf_path):
        print(f"❌ KHÔNG TÌM THẤY FILE: '{pdf_path}'")
        print(
            "👉 Hãy kéo thả file PDF vào thư mục chạy script và đổi tên thành 'cisco_design_guide.pdf' nhé!"
        )
        return

    reader = pypdf.PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f"📖 Đang đọc file PDF: '{pdf_path}' (Tổng số trang: {total_pages})...")

    raw_records = []

    for page_idx, page in enumerate(reader.pages):
        page_num = page_idx + 1
        text = page.extract_text()

        if not text:
            continue

        # Tách trang thành các đoạn văn (Paragraphs)
        paragraphs = text.split("\n\n")

        for p_idx, para in enumerate(paragraphs):
            # Làm sạch khoảng trắng dư thừa và dấu xuống dòng giữa câu
            cleaned_text = " ".join(para.split())

            # Lọc bỏ đoạn rác quá ngắn (Header, Footer, số trang...)
            if len(cleaned_text) > 30:
                raw_records.append(
                    {
                        "Document": os.path.basename(pdf_path),
                        "Page": page_num,
                        "Paragraph_ID": f"P{page_num}_{p_idx+1}",
                        "Original_Text": cleaned_text,
                    }
                )

    df = pd.DataFrame(raw_records)
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")

    print("\n" + "=" * 60)
    print("🎉 HOÀN THÀNH BÓC TÁCH DỮ LIỆU TỪ PDF!")
    print(f"📁 Dữ liệu thô được lưu tại: {output_csv}")
    print(f"📊 Tổng số đoạn văn (Raw Paragraphs) trích xuất: {len(df)}")
    print("=" * 60)

    # Hiển thị thử 3 đoạn văn đầu tiên
    print("\nMẫu dữ liệu bóc tách được:")
    print(df[["Page", "Paragraph_ID", "Original_Text"]].head(3).to_string())


if __name__ == "__main__":
    # --- THỰC THI ---
    process_cisco_pdf("cisco-campus-lan-wlan-design-guide.pdf", "research/data/cisco_raw_text.csv")
