# -*- coding: utf-8 -*-

import re
import time
import subprocess
from pathlib import Path

import uiautomator2 as u2


ADB_EXE = r"D:\platform-tools\adb.exe"
SHOPEE_PACKAGE = "com.shopee.vn"

VIDEO_DIR = Path(r"D:\platform-tools\video")
PHONE_VIDEO_PATH = "/sdcard/DCIM/Camera/000_shopee_video_001.mp4"

PLUS_X = 1000
PLUS_Y = 147
VIDEO_X = 232
VIDEO_Y = 410
NEXT_X = 285
NEXT_Y = 584

FAST_WAIT = 0.08
DEBUG = False

PRODUCT_LIMIT = 3
MIN_MATCH_WORDS = 1


def wait(sec=FAST_WAIT):
    time.sleep(sec)


def run(cmd):
    print("CMD:", cmd)
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result


def adb(cmd, device_id=None):
    if device_id:
        return run(f'"{ADB_EXE}" -s {device_id} {cmd}')
    return run(f'"{ADB_EXE}" {cmd}')


def get_device_id():
    result = adb("devices")
    devices = []

    for line in result.stdout.splitlines():
        if "\tdevice" in line:
            devices.append(line.split("\t")[0].strip())

    if not devices:
        print("Không thấy điện thoại.")
        return None

    print("Thiết bị:", devices[0])
    return devices[0]


def clean_book_title(video_path):
    name = video_path.stem
    name = name.replace(".hd", "")
    name = re.sub(r"#\S+", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def make_caption(book_title):
    return f"""Review sách: {book_title}

Mình gắn sách bên dưới nhé 👇

#sachhay #reviewsach #sachnendoc
"""


def save_debug(d, name):
    if not DEBUG:
        return

    try:
        d.screenshot(f"{name}.png")
        xml = d.dump_hierarchy()
        with open(f"{name}.xml", "w", encoding="utf-8") as f:
            f.write(xml)
        print(f"Saved: {name}.png + {name}.xml")
    except Exception as e:
        print("Không lưu được debug:", e)


def get_bounds_center(bounds):
    nums = list(map(int, re.findall(r"\d+", bounds or "")))
    if len(nums) != 4:
        return None

    x1, y1, x2, y2 = nums
    return (x1 + x2) // 2, (y1 + y2) // 2, x1, y1, x2, y2


def normalize_text(s):
    s = (s or "").lower().strip()
    s = re.sub(r"[^0-9a-zà-ỹđ\s]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s


def title_keywords(book_title):
    ignore_words = {
        "sach", "sách", "review", "full", "hd", "tap", "tập",
        "phan", "phần", "truyen", "truyện", "cuon", "cuốn"
    }

    words = []
    for w in normalize_text(book_title).split():
        if len(w) >= 3 and w not in ignore_words:
            words.append(w)

    return words


def click_text(d, text, timeout=2):
    if d(text=text).exists(timeout=timeout):
        d(text=text).click()
        wait()
        print("Clicked:", text)
        return True
    return False


def click_contains(d, text, timeout=2):
    if d(textContains=text).exists(timeout=timeout):
        d(textContains=text).click()
        wait()
        print("Clicked contains:", text)
        return True
    return False


def push_video_to_phone(device_id, video_path):
    print("Đẩy video vào điện thoại...")

    adb('shell mkdir -p "/sdcard/DCIM/Camera"', device_id)
    adb(f'shell rm -f "{PHONE_VIDEO_PATH}"', device_id)
    adb(f'push "{video_path}" "{PHONE_VIDEO_PATH}"', device_id)
    adb(f'shell touch "{PHONE_VIDEO_PATH}"', device_id)

    adb(
        "shell am broadcast "
        "-a android.intent.action.MEDIA_SCANNER_SCAN_FILE "
        f"-d file://{PHONE_VIDEO_PATH}",
        device_id,
    )

    wait(0.2)


def delete_video_from_phone(device_id):
    print("Xóa video khỏi điện thoại...")
    adb(f'shell rm -f "{PHONE_VIDEO_PATH}"', device_id)
    adb(
        "shell am broadcast "
        "-a android.intent.action.MEDIA_SCANNER_SCAN_FILE "
        f"-d file://{PHONE_VIDEO_PATH}",
        device_id,
    )
    wait(0.2)


def delete_video_from_pc(video_path):
    print("Xóa video trên máy tính...")

    try:
        video_path.unlink()
        print("Đã xóa file PC:", video_path)
    except Exception as e:
        print("Không xóa được file PC:", e)


def open_shopee(d):
    print("Mở Shopee...")
    d.app_start(SHOPEE_PACKAGE)
    wait(0.3)
    save_debug(d, "01_home")


def go_to_live_video(device_id, d):
    print("Vào Live & Video...")

    if click_text(d, "Live & Video", 4):
        return True

    adb("shell input tap 540 2190", device_id)
    wait(0.3)
    return True


def open_create_video(device_id, d):
    print("Bấm dấu + tạo video...")
    adb(f"shell input tap {PLUS_X} {PLUS_Y}", device_id)
    wait(0.5)
    return True


def open_gallery(device_id, d):
    print("Mở thư viện...")

    for txt in ["Thư viện", "Album", "Tải lên"]:
        if click_contains(d, txt, 2):
            return True

    adb("shell input tap 900 1900", device_id)
    wait(0.5)
    return True


def choose_video(device_id, d):
    print("Chọn video...")

    if d(text="Video").exists(timeout=2):
        d(text="Video").click()
        wait(0.3)

    adb(f"shell input tap {VIDEO_X} {VIDEO_Y}", device_id)
    wait(0.5)

    if d(textContains="Tiếp theo").exists(timeout=3):
        d(textContains="Tiếp theo").click()
    else:
        adb(f"shell input tap {NEXT_X} {NEXT_Y}", device_id)

    wait(0.8)

    if d(textContains="Tiếp theo").exists(timeout=2):
        d(textContains="Tiếp theo").click()
        wait(0.8)

    return True


def fill_caption(device_id, d, caption):
    print("Điền mô tả...")

    success = False

    if d(className="android.widget.EditText").exists(timeout=5):
        box = d(className="android.widget.EditText")
        box.click()
        wait(0.2)
        box.set_text(caption)
        wait(0.3)
        success = True
    else:
        adb("shell input tap 500 330", device_id)
        wait(0.2)

        if d(className="android.widget.EditText").exists(timeout=2):
            d(className="android.widget.EditText").set_text(caption)
            success = True
        else:
            d.send_keys(caption)
            success = True

    if d(text="Đồng ý").exists(timeout=2):
        d(text="Đồng ý").click()
        wait(0.3)
    else:
        adb("shell input keyevent 111", device_id)
        wait(0.3)

    return success


def open_add_product_page(device_id, d):
    print("Mở trang thêm sản phẩm...")

    for txt in ["Nhấn để thêm sản phẩm", "thêm sản phẩm", "sản phẩm"]:
        obj = d(textContains=txt)

        if obj.exists(timeout=1):
            try:
                obj.parent().click()
            except Exception:
                obj.click()

            wait(0.8)

            if d(textContains="Tìm kiếm").exists(timeout=2):
                return True

    for x, y in [(640, 570), (700, 570), (760, 570), (760, 735), (900, 735)]:
        adb(f"shell input tap {x} {y}", device_id)
        wait(0.8)

        if d(textContains="Tìm kiếm").exists(timeout=2):
            return True

    print("Không mở được trang thêm sản phẩm.")
    return False


def open_more_product_from_preview(device_id, d):
    print("Bấm Bổ sung thêm...")

    if d(textContains="Bổ sung thêm").exists(timeout=2):
        d(textContains="Bổ sung thêm").click()
        wait(0.4)
        return True

    adb("shell input tap 920 590", device_id)
    wait(0.5)

    if d(textContains="Tìm kiếm").exists(timeout=2):
        return True

    print("Không bấm được Bổ sung thêm.")
    return False


def click_all_tab(device_id, d):
    print("Chuyển sang tab Tất cả...")

    if d(text="Tất cả").exists(timeout=2):
        d(text="Tất cả").click()
        wait(0.3)
        return True

    adb("shell input tap 675 420", device_id)
    wait(0.3)
    return True


def get_product_texts(d):
    product_texts = []

    for node in d.xpath("//*").all():
        text = (node.attrib.get("text") or "").strip()
        bounds = node.attrib.get("bounds", "")
        center = get_bounds_center(bounds)

        if not text or not center:
            continue

        cx, cy, x1, y1, x2, y2 = center

        if y1 < 580 or x1 < 250 or x2 < 800:
            continue

        low = normalize_text(text)

        if any(k in low for k in [
            "tỷ lệ hoa hồng", "đã bán", "₫", "%",
            "thêm", "phổ biến", "mới nhất", "bán chạy",
            "giá", "tất cả", "shop của tôi"
        ]):
            continue

        product_texts.append((y1, text))

    product_texts.sort(key=lambda x: x[0])
    return [text for _, text in product_texts]


def has_matching_product(d, book_title):
    keywords = title_keywords(book_title)

    if not keywords:
        print("Tên sách không có keyword đủ mạnh.")
        return False

    products = get_product_texts(d)
    top_products = products[:PRODUCT_LIMIT]

    print("Keyword tên sách:", keywords)
    print("Top sản phẩm kiểm tra:")

    for i, text in enumerate(top_products, 1):
        print(f"{i}. {text[:120]}")

    for text in top_products:
        low = normalize_text(text)
        hit_count = sum(1 for w in keywords if w in low)

        if hit_count >= MIN_MATCH_WORDS:
            print("Có sản phẩm khớp:", text[:120])
            return True

    print("Có sản phẩm nhưng không khớp tên tìm kiếm.")
    return False


def search_product(device_id, d, book_title):
    print("Tìm sản phẩm:", book_title)

    if d(textContains="Tìm kiếm sản phẩm").exists(timeout=3):
        d(textContains="Tìm kiếm sản phẩm").click()
    elif d(textContains="Tìm kiếm").exists(timeout=3):
        d(textContains="Tìm kiếm").click()
    elif d(className="android.widget.EditText").exists(timeout=2):
        d(className="android.widget.EditText").click()
    else:
        adb("shell input tap 500 275", device_id)

    wait(0.3)

    if d(className="android.widget.EditText").exists(timeout=3):
        box = d(className="android.widget.EditText")
        box.click()
        wait(0.1)
        try:
            box.clear_text()
        except Exception:
            pass
        wait(0.1)
        box.set_text(book_title)
    else:
        d.send_keys(book_title)

    wait(0.3)

    if d(text="Tìm kiếm").exists(timeout=1):
        d(text="Tìm kiếm").click()
    elif d(textContains="Tìm kiếm").exists(timeout=1):
        d(textContains="Tìm kiếm").click()
    else:
        d.press("enter")

    found = False

    for _ in range(20):
        if d(text="Thêm").exists(timeout=0.3):
            found = True
            break
        wait(0.2)

    adb("shell input keyevent 111", device_id)
    wait(0.2)

    if not found:
        print("Không có kết quả sản phẩm.")
        return False

    if not has_matching_product(d, book_title):
        return False

    return True


def get_add_buttons(d):
    add_buttons = []

    for node in d.xpath("//*").all():
        text = (node.attrib.get("text") or "").strip()
        desc = (node.attrib.get("content-desc") or "").strip()
        bounds = node.attrib.get("bounds", "")
        center = get_bounds_center(bounds)

        if not center:
            continue

        cx, cy, x1, y1, x2, y2 = center

        if text != "Thêm" and desc != "Thêm":
            continue

        if y1 < 580:
            continue

        if cx < 750:
            continue

        add_buttons.append((y1, node, bounds))

    add_buttons.sort(key=lambda x: x[0])
    return add_buttons


def choose_product_by_index(device_id, d, index):
    print("Chọn sản phẩm thứ:", index + 1)

    add_buttons = get_add_buttons(d)

    if index >= len(add_buttons):
        print("Không đủ sản phẩm để chọn:", index + 1)
        return False

    _, node, bounds = add_buttons[index]

    try:
        node.click()
        wait(0.4)
        print("Đã click nút Thêm:", bounds)
        return True
    except Exception as e:
        print("Click node lỗi:", e)

    center = get_bounds_center(bounds)

    if center:
        cx, cy, x1, y1, x2, y2 = center
        adb(f"shell input tap {cx} {cy}", device_id)
        wait(0.4)
        return True

    return False


def confirm_after_add(d):
    for txt in ["Xong", "Hoàn tất", "Đồng ý", "Tiếp theo", "OK"]:
        if d(textContains=txt).exists(timeout=2):
            d(textContains=txt).click()
            wait(0.5)
            print("Clicked confirm:", txt)
            return True

    return True


def add_one_product(device_id, d, book_title, index):
    print("=" * 60)
    print(f"THÊM SẢN PHẨM {index + 1}/{PRODUCT_LIMIT}")
    print("=" * 60)

    if index == 0:
        if not open_add_product_page(device_id, d):
            return False
    else:
        if not open_more_product_from_preview(device_id, d):
            return False

    click_all_tab(device_id, d)

    if not search_product(device_id, d, book_title):
        return False

    if not choose_product_by_index(device_id, d, index):
        return False

    confirm_after_add(d)
    return True


def add_products(device_id, d, book_title):
    for i in range(PRODUCT_LIMIT):
        ok = add_one_product(device_id, d, book_title, i)

        if not ok:
            print("Không thêm được sản phẩm số:", i + 1)
            return False

        wait(0.4)

    print("Đã thêm xong sản phẩm.")
    return True


def publish_video(device_id, d):
    print("Chuẩn bị bấm Đăng...")

    if d(text="Đăng").exists(timeout=3):
        d(text="Đăng").click()
        wait(3)
        print("Đã bấm Đăng.")
        return True

    if d(textContains="Đăng").exists(timeout=3):
        d(textContains="Đăng").click()
        wait(3)
        print("Đã bấm Đăng.")
        return True

    adb("shell input tap 625 2050", device_id)
    wait(3)
    print("Đã bấm Đăng bằng tọa độ fallback.")
    return True


def back_to_safe_start(device_id, d):
    print("Quay về trạng thái an toàn...")
    for _ in range(3):
        adb("shell input keyevent 4", device_id)
        wait(0.3)

    open_shopee(d)
    wait(0.5)
    
def restart_shopee(device_id, d):
    print("Khởi động lại Shopee...")

    # kill app
    adb(f"shell am force-stop {SHOPEE_PACKAGE}", device_id)
    wait(1)

    # mở lại
    d.app_start(SHOPEE_PACKAGE)

    # đợi app load
    wait(3)

    print("Đã mở lại Shopee.")
    return True
def close_whatsapp_share_popup(device_id, d):
    print("Kiểm tra popup chia sẻ WhatsApp...")

    for _ in range(10):
        if d(text="Hủy").exists(timeout=0.5):
            d(text="Hủy").click()
            wait(0.5)
            print("Đã bấm Hủy popup WhatsApp.")
            return True

        if d(textContains="Chia sẻ lên WhatsApp").exists(timeout=0.3):
            adb("shell input tap 300 1355", device_id)  # tọa độ nút Hủy
            wait(0.5)
            print("Đã bấm Hủy bằng tọa độ.")
            return True

        wait(0.3)

    print("Không thấy popup WhatsApp.")
    return False
def skip_video(device_id, d, video_path, reason):
    print("=" * 60)
    print("BỎ QUA VIDEO:", video_path)
    print("Lý do:", reason)
    print("=" * 60)

    delete_video_from_phone(device_id)
    delete_video_from_pc(video_path)

    restart_shopee(device_id, d)

def main():
    device_id = get_device_id()
    if not device_id:
        return

    d = u2.connect(device_id)

    open_shopee(d)

    while True:
        videos = list(VIDEO_DIR.glob("*.mp4"))

        if not videos:
            print("Không còn video nào trong:", VIDEO_DIR)
            break

        video_path = max(videos, key=lambda p: p.stat().st_mtime)
        book_title = clean_book_title(video_path)
        caption = make_caption(book_title)

        print("=" * 60)
        print("BẮT ĐẦU ĐĂNG VIDEO:", video_path)
        print("Tên sách:", book_title)
        print("=" * 60)

        push_video_to_phone(device_id, video_path)

        try:
            go_to_live_video(device_id, d)
            open_create_video(device_id, d)
            open_gallery(device_id, d)
            choose_video(device_id, d)

            if not fill_caption(device_id, d, caption):
                skip_video(device_id, d, video_path, "Không nhập được caption")
                continue

            if not add_products(device_id, d, book_title):
                skip_video(device_id, d, video_path, "Không có sản phẩm khớp tên sách")
                continue

            if not publish_video(device_id, d):
                print("Không đăng được video. Dừng bot.")
                break

            wait(8)

            delete_video_from_phone(device_id)
            delete_video_from_pc(video_path)

            print("=" * 60)
            print("ĐÃ ĐĂNG XONG:", video_path)
            print("TIẾP TỤC VIDEO TIẾP THEO...")
            print("=" * 60)

            wait(1)
            open_shopee(d)

        except Exception as e:
            print("Lỗi khi xử lý video:", e)
            skip_video(device_id, d, video_path, "Lỗi ngoài ý muốn")
            continue

    print("=" * 60)
    print("HOÀN TẤT. ĐÃ XỬ LÝ HẾT VIDEO.")
    print("=" * 60)


if __name__ == "__main__":
    main()