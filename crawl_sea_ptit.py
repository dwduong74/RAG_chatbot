# -*- coding: utf-8 -*-
"""
Script thu thập toàn bộ dữ liệu từ cổng thông tin Khoa Kỹ thuật Điện tử 1 (SEA - PTIT)
Nguồn: https://sea.ptit.edu.vn/
Giao thức: WordPress REST API v2 (/wp-json/wp/v2/)
"""

import os
import sys
import json
import ssl
import time
import urllib.request
import re
from bs4 import BeautifulSoup

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_URL = "https://sea.ptit.edu.vn"
API_BASE = f"{BASE_URL}/wp-json/wp/v2"
OUTPUT_DIR = "data_sea_ptit"
DOCS_DIR = os.path.join(OUTPUT_DIR, "documents")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            headers = dict(resp.headers)
            body = resp.read().decode("utf-8", errors="ignore")
            data = json.loads(body)
            total = int(headers.get("X-WP-Total", headers.get("x-wp-total", len(data))))
            total_pages = int(headers.get("X-WP-TotalPages", headers.get("x-wp-totalpages", 1)))
            return data, total, total_pages
    except Exception as e:
        print(f"[!] Lỗi khi tải {url}: {e}")
        return [], 0, 0

def clean_html(html_content):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Loại bỏ script, style, form, iframe
    for tag in soup(["script", "style", "form", "iframe", "noscript"]):
        tag.decompose()
        
    # Chuyển đổi các thẻ link thành text có link
    for a in soup.find_all("a", href=True):
        link_text = a.get_text().strip()
        href = a["href"].strip()
        if link_text and href.startswith("http") and not href.endswith((".png", ".jpg", ".jpeg", ".gif", ".css", ".js")):
            a.replace_with(f"{link_text} ({href})")
            
    # Lấy text với các ngắt dòng hợp lý
    text = soup.get_text(separator="\n")
    
    # Chuẩn hóa khoảng trắng
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in text.split("\n")]
    # Gộp các dòng trống liên tiếp
    cleaned_lines = []
    prev_blank = False
    for line in lines:
        if not line:
            if not prev_blank:
                cleaned_lines.append("")
                prev_blank = True
        else:
            cleaned_lines.append(line)
            prev_blank = False
            
    return "\n".join(cleaned_lines).strip()

def sanitize_filename(name):
    clean = re.sub(r'[\\/*?:"<>|]', '_', name)
    clean = re.sub(r'[\s_]+', '_', clean)
    return clean[:80].strip('_')

def fetch_all_items(endpoint_name):
    print(f"\n[*] Đang thu thập danh mục '{endpoint_name}'...")
    all_items = []
    page = 1
    per_page = 100
    
    while True:
        url = f"{API_BASE}/{endpoint_name}?per_page={per_page}&page={page}"
        print(f"  -> Tải trang {page}: {url}")
        items, total, total_pages = fetch_json(url)
        if not items:
            break
            
        all_items.extend(items)
        print(f"     Nhận {len(items)} mục. Đã tải {len(all_items)}/{total} mục.")
        
        if page >= total_pages:
            break
        page += 1
        time.sleep(0.5)
        
    return all_items

def main():
    print("=" * 80)
    print(" BẮT ĐẦU THU THẬP DỮ LIỆU KHOA KỸ THUẬT ĐIỆN TỬ 1 (SEA - PTIT)")
    print(f" URL: {BASE_URL}")
    print("=" * 80)
    
    os.makedirs(DOCS_DIR, exist_ok=True)
    
    # 1. Thu thập danh mục (Categories) để map ID sang tên
    print("\n[*] Đang lấy danh mục (Categories)...")
    cats, _, _ = fetch_json(f"{API_BASE}/categories?per_page=100")
    cat_map = {c["id"]: c["name"] for c in cats}
    print(f"[OK] Đã lấy {len(cat_map)} danh mục chuyên đề.")
    for cid, cname in cat_map.items():
        print(f"  - ID {cid}: {cname}")
        
    # 2. Thu thập bài viết (Posts)
    posts = fetch_all_items("posts")
    print(f"[OK] Đã thu thập thành công {len(posts)} bài viết tin tức và NCKH.")
    
    # 3. Thu thập trang tĩnh (Pages)
    pages = fetch_all_items("pages")
    print(f"[OK] Đã thu thập thành công {len(pages)} trang tĩnh (giảng viên, đào tạo, lab, v.v.).")
    
    # 4. Xử lý làm sạch và lưu trữ
    print("\n[*] Đang làm sạch nội dung và lưu trữ tệp Markdown...")
    all_documents = []
    
    # Xử lý Posts
    for p in posts:
        pid = p["id"]
        slug = p.get("slug", f"post_{pid}")
        raw_title = p.get("title", {}).get("rendered", "")
        clean_title = BeautifulSoup(raw_title, "html.parser").get_text().strip()
        link = p.get("link", f"{BASE_URL}/?p={pid}")
        date_str = p.get("date", "")
        modified_str = p.get("modified", "")
        
        post_cats = [cat_map.get(cid, f"Cat_{cid}") for cid in p.get("categories", [])]
        category_str = ", ".join(post_cats) if post_cats else "Tin tức chung"
        
        raw_content = p.get("content", {}).get("rendered", "")
        raw_excerpt = p.get("excerpt", {}).get("rendered", "")
        
        clean_content_text = clean_html(raw_content)
        clean_excerpt_text = clean_html(raw_excerpt)
        
        if not clean_content_text and clean_excerpt_text:
            clean_content_text = clean_excerpt_text
            
        if not clean_content_text:
            continue
            
        filename = f"post_{pid}_{sanitize_filename(slug)}.md"
        filepath = os.path.join(DOCS_DIR, filename)
        
        md_text = f"""---
id: {pid}
type: post
title: "{clean_title}"
url: "{link}"
date: "{date_str}"
modified: "{modified_str}"
category: "{category_str}"
slug: "{slug}"
---

# {clean_title}

- **Nguồn bài viết**: [{link}]({link})
- **Ngày đăng**: {date_str}
- **Chuyên mục**: {category_str}

## Nội dung chi tiết:

{clean_content_text}
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_text)
            
        all_documents.append({
            "id": pid,
            "type": "post",
            "title": clean_title,
            "url": link,
            "date": date_str,
            "category": category_str,
            "filename": filename,
            "filepath": filepath,
            "word_count": len(clean_content_text.split())
        })
        
    # Xử lý Pages
    for p in pages:
        pid = p["id"]
        slug = p.get("slug", f"page_{pid}")
        raw_title = p.get("title", {}).get("rendered", "")
        clean_title = BeautifulSoup(raw_title, "html.parser").get_text().strip()
        link = p.get("link", f"{BASE_URL}/?page_id={pid}")
        date_str = p.get("date", "")
        modified_str = p.get("modified", "")
        
        category_str = "Trang thông tin / Giới thiệu / Đào tạo"
        if "pgs" in slug or "ts-" in slug or "th-s" in slug or "thay" in slug or "co-" in slug:
            category_str = "Đội ngũ Giảng viên & Nhà khoa học"
        elif "chuong-trinh" in slug or "dao-tao" in slug:
            category_str = "Chương trình Đào tạo"
        elif "lab" in slug or "phong" in slug:
            category_str = "Phòng Thí nghiệm & Trang thiết bị"
        elif "bai-bao" in slug or "nghien-cuu" in slug or "de-tai" in slug:
            category_str = "Công bố Khoa học & Dự án"
        elif "sinh-vien" in slug or "clb" in slug or "doan" in slug:
            category_str = "Sinh viên & Câu lạc bộ"
        elif "doanh-nghiep" in slug or "hop-tac" in slug:
            category_str = "Hợp tác Doanh nghiệp"
            
        raw_content = p.get("content", {}).get("rendered", "")
        clean_content_text = clean_html(raw_content)
        
        if not clean_content_text:
            continue
            
        filename = f"page_{pid}_{sanitize_filename(slug)}.md"
        filepath = os.path.join(DOCS_DIR, filename)
        
        md_text = f"""---
id: {pid}
type: page
title: "{clean_title}"
url: "{link}"
date: "{date_str}"
modified: "{modified_str}"
category: "{category_str}"
slug: "{slug}"
---

# {clean_title}

- **Nguồn trang**: [{link}]({link})
- **Ngày cập nhật**: {modified_str or date_str}
- **Phân loại**: {category_str}

## Nội dung chi tiết:

{clean_content_text}
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_text)
            
        all_documents.append({
            "id": pid,
            "type": "page",
            "title": clean_title,
            "url": link,
            "date": date_str,
            "category": category_str,
            "filename": filename,
            "filepath": filepath,
            "word_count": len(clean_content_text.split())
        })

    # Lưu tệp tổng kết summary.json
    summary_path = os.path.join(OUTPUT_DIR, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(all_documents, f, ensure_ascii=False, indent=2)
        
    total_words = sum(d["word_count"] for d in all_documents)
    print("\n" + "=" * 80)
    print(f"[THÀNH CÔNG] Thu thập hoàn tất:")
    print(f" - Tổng số tài liệu hợp lệ đã lưu: {len(all_documents)} tệp Markdown")
    print(f" - Trong đó: {sum(1 for d in all_documents if d['type'] == 'post')} bài viết, {sum(1 for d in all_documents if d['type'] == 'page')} trang tĩnh")
    print(f" - Tổng dung lượng từ vựng: {total_words:,} từ tiếng Việt")
    print(f" - Thư mục lưu trữ: {os.path.abspath(DOCS_DIR)}")
    print(f" - Tệp chỉ mục tổng quan: {os.path.abspath(summary_path)}")
    print("=" * 80)

if __name__ == "__main__":
    main()
