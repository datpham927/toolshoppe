# Auto-cleaned version: debug screenshot/XML capture removed, main logic kept.
import re
import time
import random
import requests
import subprocess
from pathlib import Path
from datetime import datetime
from io import BytesIO, StringIO
import pandas as pd
import uiautomator2 as u2
ADB_EXE = 'D:\\platform-tools\\adb.exe'
FFMPEG_EXE = r'D:\tool\auto-video-editor\node_modules\ffmpeg-static\ffmpeg.exe'
FFPROBE_EXE = r'D:\tool\auto-video-editor\node_modules\ffprobe-static\bin\win32\x64\ffprobe.exe'
EDIT_VIDEO_BEFORE_POST = True
EDIT_TARGET_DURATION = 12.0
EDIT_WIDTH = 1080
EDIT_HEIGHT = 1920
EDIT_FPS = 30
EDIT_TRANSITION_DURATION = 0.22
SHOPEE_PACKAGE = 'com.shopee.vn'
VIDEO_DIR = Path('D:\\platform-tools\\video')
VIDEO_DIR.mkdir(parents=True, exist_ok=True)
PHONE_VIDEO_PATH = '/sdcard/DCIM/Camera/000_shopee_video_001.mp4'
FAST_WAIT = 0.3
DOWNLOAD_RETRY = 3
PUBLISH_AFTER_ADD_PRODUCT = True
STOP_ON_SELECTOR_ERROR = False
PICK_FIRST_VISIBLE_VIDEO = True
SHEET_ID = '1nKcbh7666kDerwnLSM8r5nTgxnNsnzm_fUdbnO1DOS8'
SHEET_GID = '1569233489'
GOOGLE_SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx&gid={SHEET_GID}'
SELECTORS = {'home_popup_close': [{'by': 'resource_id', 'value': 'com.shopee.vn:id/img_close'}, {'by': 'resource_id', 'value': 'com.shopee.vn:id/iv_close'}, {'by': 'desc_contains', 'value': 'close'}, {'by': 'desc_contains', 'value': 'Close'}, {'by': 'desc_contains', 'value': 'đóng'}, {'by': 'desc_contains', 'value': 'Đóng'}, {'by': 'xpath', 'value': '//*[@clickable="true" and (@bounds="[860,480][1000,620]" or contains(@content-desc, "close") or contains(@content-desc, "Close"))]'}, {'by': 'xpath', 'value': '(//*[@clickable="true" and contains(@class, "ImageView")])[last()]'}], 'live_video_tab': [{'by': 'desc', 'value': 'Live & Video'}, {'by': 'desc_contains', 'value': 'Live & Video'}, {'by': 'text', 'value': 'Live & Video'}, {'by': 'text_contains', 'value': 'Live & Video'}, {'by': 'text_contains', 'value': 'Video'}, {'by': 'xpath', 'value': '//*[contains(@text, "Live") or contains(@content-desc, "Live")]'}], 'create_plus': [{'by': 'desc_contains', 'value': 'click top right create icon'}, {'by': 'desc_contains', 'value': 'top right create icon'}, {'by': 'desc_contains', 'value': 'create icon'}, {'by': 'resource_id', 'value': 'com.shopee.vn:id/iv_create'}, {'by': 'resource_id', 'value': 'com.shopee.vn:id/iv_add'}, {'by': 'xpath', 'value': '//*[@content-desc="click top right create icon"]'}, {'by': 'xpath', 'value': '//*[contains(@content-desc, "create icon")]'}, {'by': 'xpath', 'value': '//*[@clickable="true" and contains(@class, "ImageView") and contains(@bounds, "][1080,")]'}], 'gallery_entrance': [{'by': 'resource_id', 'value': 'com.shopee.vn:id/ll_gallery_entrance'}, {'by': 'resource_id', 'value': 'com.shopee.vn:id/tv_gallery_entrance'}, {'by': 'text', 'value': 'Thư viện'}, {'by': 'text_contains', 'value': 'Thư viện'}, {'by': 'desc', 'value': 'Thư viện'}, {'by': 'desc_contains', 'value': 'Thư viện'}, {'by': 'text_contains', 'value': 'Album'}, {'by': 'text_contains', 'value': 'Tải lên'}, {'by': 'xpath', 'value': '//*[contains(@text, "Thư viện") or contains(@content-desc, "Thư viện")]'}], 'gallery_video_tab': [{'by': 'desc', 'value': 'Video'}, {'by': 'desc_contains', 'value': 'Video'}, {'by': 'text', 'value': 'Video'}, {'by': 'text_contains', 'value': 'Video'}, {'by': 'xpath', 'value': '//*[@content-desc="Video" and (@clickable="true" or @focusable="true")]'}, {'by': 'xpath', 'value': '//*[contains(@text, "Video") or contains(@content-desc, "Video")]'}], 'oneclip': [{'by': 'text_contains', 'value': 'OneClip'}, {'by': 'text_contains', 'value': 'oneclip'}, {'by': 'desc_contains', 'value': 'OneClip'}, {'by': 'xpath', 'value': '//*[contains(@text, "OneClip") or contains(@content-desc, "OneClip")]'}], 'next_button': [{'by': 'resource_id', 'value': 'com.shopee.vn:id/tv_compress'}, {'by': 'resource_id', 'value': 'com.shopee.vn:id/tv_next'}, {'by': 'text', 'value': 'Tiếp theo'}, {'by': 'text_contains', 'value': 'Tiếp theo'}, {'by': 'text_contains', 'value': 'Tiep theo'}, {'by': 'text_contains', 'value': 'Next'}, {'by': 'desc_contains', 'value': 'Tiếp theo'}, {'by': 'xpath', 'value': '//*[contains(@text, "Tiếp theo") or contains(@text, "Next") or contains(@content-desc, "Tiếp theo")]'}], 'caption_box': [{'by': 'resource_id', 'value': 'com.shopee.vn:id/et_caption'}, {'by': 'class', 'value': 'android.widget.EditText'}, {'by': 'xpath', 'value': '//android.widget.EditText'}, {'by': 'xpath', 'value': '//*[contains(@class, "EditText")]'}], 'confirm_ok': [{'by': 'text', 'value': 'Đồng ý'}, {'by': 'text_contains', 'value': 'Đồng ý'}, {'by': 'text_contains', 'value': 'OK'}, {'by': 'text_contains', 'value': 'Done'}], 'add_product_entry': [{'by': 'text_contains', 'value': 'Nhấn để thêm sản phẩm'}, {'by': 'text_contains', 'value': 'Thêm sản phẩm'}, {'by': 'text_contains', 'value': 'thêm sản phẩm'}, {'by': 'text_contains', 'value': 'sản phẩm'}, {'by': 'desc_contains', 'value': 'Thêm sản phẩm'}, {'by': 'xpath', 'value': '//*[contains(@text, "sản phẩm") or contains(@content-desc, "sản phẩm")]'}], 'product_link_icon': [{'by': 'resource_id', 'value': 'com.shopee.vn:id/iv_link'}, {'by': 'resource_id', 'value': 'com.shopee.vn:id/link_icon'}, {'by': 'xpath', 'value': '//*[@class="android.widget.ImageView" and @visible-to-user="true"]'}], 'link_input': [{'by': 'resource_id', 'value': 'com.shopee.vn:id/et_link'}, {'by': 'text_contains', 'value': 'http'}, {'by': 'class', 'value': 'android.widget.EditText'}, {'by': 'xpath', 'value': '//android.widget.EditText'}, {'by': 'xpath', 'value': '//*[contains(@class, "EditText")]'}], 'import_button': [{'by': 'text', 'value': 'Nhập'}, {'by': 'text_contains', 'value': 'Nhập'}, {'by': 'text_contains', 'value': 'Nhap'}, {'by': 'text_contains', 'value': 'Import'}, {'by': 'xpath', 'value': '//*[contains(@text, "Nhập") or contains(@text, "Import")]'}], 'select_all': [{'by': 'text_contains', 'value': 'Chọn tất cả'}, {'by': 'text_contains', 'value': 'Chon tat ca'}, {'by': 'text_contains', 'value': 'Tất cả'}, {'by': 'text_contains', 'value': 'Tat ca'}, {'by': 'xpath', 'value': '//*[contains(@text, "Chọn tất cả") or contains(@text, "Tất cả")]'}], 'add_selected': [{'by': 'text_contains', 'value': 'Thêm('}, {'by': 'text_contains', 'value': 'Them('}, {'by': 'text_contains', 'value': 'Thêm'}, {'by': 'text_contains', 'value': 'Them'}, {'by': 'text_contains', 'value': 'Add'}, {'by': 'xpath', 'value': '//*[contains(@text, "Thêm") or contains(@text, "Add")]'}], 'post_button': [{'by': 'text_contains', 'value': 'Đăng video'}, {'by': 'text_contains', 'value': 'Dang video'}, {'by': 'text', 'value': 'Đăng'}, {'by': 'text_contains', 'value': 'Đăng'}, {'by': 'text_contains', 'value': 'Dang'}, {'by': 'text_contains', 'value': 'Post'}, {'by': 'xpath', 'value': '//*[contains(@text, "Đăng") or contains(@text, "Post")]'}], 'cancel_popup': [{'by': 'text_contains', 'value': 'Hủy'}, {'by': 'text_contains', 'value': 'Huy'}, {'by': 'text_contains', 'value': 'Cancel'}, {'by': 'text_contains', 'value': 'Không'}, {'by': 'text_contains', 'value': 'Khong'}]}

def wait(sec=FAST_WAIT):
    time.sleep(sec)

def run(cmd):
    print('CMD:', cmd)
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
    result = adb('devices')
    devices = []
    for line in result.stdout.splitlines():
        if '\tdevice' in line:
            devices.append(line.split('\t')[0].strip())
    if not devices:
        print('Không thấy điện thoại.')
        print('Hãy kiểm tra:')
        print(f'"{ADB_EXE}" devices')
        return None
    print('Thiết bị:', devices[0])
    return devices[0]

def press_escape(device_id, delay=FAST_WAIT):
    adb('shell input keyevent 111', device_id)
    wait(delay)

def press_back(device_id, delay=FAST_WAIT):
    adb('shell input keyevent 4', device_id)
    wait(delay)

def sanitize_file_name(name):
    name = name or 'debug'
    name = re.sub('[<>:"/\\\\|?*]', '', name)
    name = name.replace('\n', ' ').replace('\r', ' ')
    name = re.sub('\\s+', ' ', name)
    return name.strip()[:120] or 'debug'

def clean_caption(title):
    title = title or ''
    title = title.strip()
    title = re.sub('\\s+', ' ', title)
    return title

def parse_bounds(bounds_text):
    """
    "[0,363][270,720]" -> (0, 363, 270, 720)
    """
    m = re.match('\\[(\\d+),(\\d+)\\]\\[(\\d+),(\\d+)\\]', bounds_text or '')
    if not m:
        return None
    return tuple((int(x) for x in m.groups()))

def center_of_bounds(bounds):
    left, top, right, bottom = bounds
    return ((left + right) // 2, (top + bottom) // 2)
CURRENT_DEBUG_DIR = None

def get_selector_obj(d, selector):
    by = selector.get('by')
    value = selector.get('value')
    if by == 'text':
        return d(text=value)
    if by == 'text_contains':
        return d(textContains=value)
    if by == 'desc':
        return d(description=value)
    if by == 'desc_contains':
        return d(descriptionContains=value)
    if by == 'resource_id':
        return d(resourceId=value)
    if by == 'class':
        return d(className=value)
    if by == 'xpath':
        return d.xpath(value)
    raise ValueError(f'Selector không hỗ trợ: {selector}')

def selector_exists(obj, selector):
    try:
        if selector.get('by') == 'xpath':
            return bool(obj.exists)
        return bool(obj.exists(timeout=0))
    except Exception:
        return False

def selector_click(obj, selector):
    obj.click()

def wait_find_selector(d, key, timeout=15, interval=0.3):
    selectors = SELECTORS.get(key, [])
    if not selectors:
        raise Exception(f'Chưa khai báo selector key: {key}')
    end = time.time() + timeout
    last_error = None
    while time.time() < end:
        for selector in selectors:
            try:
                obj = get_selector_obj(d, selector)
                if selector_exists(obj, selector):
                    print(f'FOUND {key}: {selector}')
                    return (obj, selector)
            except Exception as e:
                last_error = e
        time.sleep(interval)
    raise Exception(f"Không tìm thấy selector key='{key}' sau {timeout}s. Hãy kiểm tra lại SELECTORS. Last error: {last_error}")

def click_ui(d, key, timeout=15, after_click=1.0, optional=False):
    """
    Click theo UI object.
    Không dùng tọa độ cố định.
    """
    print('=' * 60)
    print('CLICK STEP:', key)
    print('=' * 60)
    try:
        obj, selector = wait_find_selector(d, key, timeout=timeout)
        selector_click(obj, selector)
        print(f'CLICKED {key}: {selector}')
        wait(after_click)
        return True
    except Exception as e:
        if optional:
            print(f'Optional click failed: {key} - {e}')
            return False
        raise

def input_ui(d, key, text, timeout=10):
    """
    Nhập text vào EditText.
    """
    print('=' * 60)
    print('INPUT STEP:', key)
    print('=' * 60)
    obj, selector = wait_find_selector(d, key, timeout=timeout)
    try:
        obj.click()
        wait(0.5)
        try:
            obj.clear_text()
            wait(0.5)
        except Exception:
            pass
        try:
            obj.set_text(text)
        except Exception:
            d.send_keys(text)
        wait(0.8)
        return True
    except Exception as e:
        raise Exception(f"Nhập text thất bại key='{key}', selector={selector}, error={e}")

def wait_text_any(d, texts, timeout=10):
    if isinstance(texts, str):
        texts = [texts]
    end = time.time() + timeout
    while time.time() < end:
        for text in texts:
            try:
                if d(textContains=text).exists(timeout=0):
                    print('Đã thấy text:', text)
                    return True
            except Exception:
                pass
        time.sleep(0.3)
    return False

def click_dynamic_center(d, obj, label, after_click=1.0):
    """
    Click vào tâm object theo bounds hiện tại của XML.
    Đây không phải tọa độ cố định.
    """
    print('=' * 60)
    print('DYNAMIC CLICK:', label)
    print('=' * 60)
    try:
        info = obj.info
        bounds = info.get('bounds')
        if isinstance(bounds, dict):
            left = int(bounds.get('left', 0))
            top = int(bounds.get('top', 0))
            right = int(bounds.get('right', 0))
            bottom = int(bounds.get('bottom', 0))
        else:
            parsed = parse_bounds(str(bounds))
            if not parsed:
                raise Exception(f'Không parse được bounds: {bounds}')
            left, top, right, bottom = parsed
        x = (left + right) // 2
        y = (top + bottom) // 2
        print(f'Click dynamic center {label}: bounds=({left},{top},{right},{bottom}), center=({x},{y})')
        d.click(x, y)
        wait(after_click)
        return True
    except Exception as e:
        raise Exception(f'Dynamic click failed {label}: {e}')

def load_jobs_from_google_sheet_readonly():
    print('Đang đọc Google Sheet chỉ đọc...')

    if not SHEET_ID:
        raise Exception('Bạn chưa điền SHEET_ID trong code.')

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/123 Safari/537.36'
        )
    }

    xlsx_url = (
        f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export'
        f'?format=xlsx&gid={SHEET_GID}'
    )
    csv_url = (
        f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq'
        f'?tqx=out:csv&gid={SHEET_GID}'
    )

    df = None
    errors = []

    try:
        print('Thử tải Google Sheet dạng XLSX...')
        print('URL:', xlsx_url)

        response = requests.get(
            xlsx_url,
            headers=headers,
            timeout=30,
            allow_redirects=True,
        )

        content_type = response.headers.get('Content-Type', '')
        print('HTTP:', response.status_code)
        print('Content-Type:', content_type)

        if response.status_code == 200:
            content_lower = response.content[:100].lower()

            if b'<html' not in content_lower and b'<!doctype html' not in content_lower:
                try:
                    df = pd.read_excel(
                        BytesIO(response.content),
                        engine='openpyxl',
                    )
                    print('Đọc XLSX thành công.')
                except Exception as e:
                    errors.append(f'Đọc XLSX lỗi: {e}')
            else:
                errors.append('XLSX trả về HTML thay vì file Excel.')
        else:
            body = response.text[:500].replace('\n', ' ')
            errors.append(f'XLSX HTTP {response.status_code}: {body}')
    except Exception as e:
        errors.append(f'Tải XLSX lỗi: {e}')

    if df is None:
        try:
            print('XLSX không đọc được, thử fallback CSV...')
            print('URL:', csv_url)

            response = requests.get(
                csv_url,
                headers=headers,
                timeout=30,
                allow_redirects=True,
            )

            content_type = response.headers.get('Content-Type', '')
            print('HTTP:', response.status_code)
            print('Content-Type:', content_type)

            if response.status_code != 200:
                body = response.text[:500].replace('\n', ' ')
                raise Exception(f'CSV HTTP {response.status_code}: {body}')

            text_data = response.content.decode('utf-8-sig', errors='replace')
            stripped = text_data.lstrip().lower()

            if stripped.startswith('<!doctype html') or stripped.startswith('<html'):
                raise Exception(
                    'Google trả về HTML thay vì CSV. '
                    'Sheet có thể chưa cho phép truy cập bằng link.'
                )

            df = pd.read_csv(StringIO(text_data))
            print('Đọc CSV thành công.')

        except Exception as e:
            errors.append(f'Tải/đọc CSV lỗi: {e}')

    if df is None:
        print('=' * 60)
        print('KHÔNG ĐỌC ĐƯỢC GOOGLE SHEET')
        print('=' * 60)
        for item in errors:
            print('-', item)
        print('=' * 60)
        raise Exception(
            'Không tải được Google Sheet. '
            'Kiểm tra SHEET_ID, SHEET_GID và quyền chia sẻ của Sheet.'
        )

    df.columns = [str(c).strip().lower() for c in df.columns]
    print('Columns:', list(df.columns))

    if 'tiktok' not in df.columns:
        raise Exception(
            'Google Sheet phải có cột tên là: tiktok. '
            f'Các cột hiện có: {list(df.columns)}'
        )

    jobs = []

    for _, row in df.iterrows():
        tiktok = str(row.get('tiktok', '')).strip()

        if not tiktok or tiktok.lower() == 'nan':
            continue

        shopee_links = []

        for col in df.columns:
            col_name = str(col).strip().lower()

            if col_name.startswith('shopee'):
                value = str(row.get(col, '')).strip()

                if value and value.lower() != 'nan':
                    shopee_links.append(value)

        jobs.append({
            'link_tiktok': tiktok,
            'shopee_links': shopee_links,
        })

    print('Số job lấy được:', len(jobs))
    return jobs

def remove_tiktok_words(text):
    if not text:
        return text

    # Xóa các từ liên quan TikTok (không phân biệt hoa/thường)
    patterns = [
        r'\btiktok\b',
        r'\btik\s*tok\b',
        r'\btik_tok\b',
        r'\btik-tok\b',
        r'\btt\b',
    ]

    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # Xóa khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text).strip(' -_|')

    return text
def download_tiktok(url, folder):
    print('=' * 60)
    print('Đang tải TikTok:', url)
    api = f'https://www.tikwm.com/api/?url={url}'
    for retry in range(DOWNLOAD_RETRY):
        try:
            print(f'Thử tải lần {retry + 1}/{DOWNLOAD_RETRY}')
            res = requests.get(api, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/123 Safari/537.36'}, timeout=20)
            data = res.json()
            if not data.get('data'):
                print('Không lấy được data TikTok, thử lại...')
                wait(1)
                continue
            info = data['data']
            raw_title = info.get('title') or 'tiktok_video'
            title = clean_caption(raw_title)
            title = remove_tiktok_words(title)
            safe_title = sanitize_file_name(title)
            video_url = info.get('play') or info.get('wmplay')
            if not video_url:
                print('Không có link video trong TikTok API.')
                wait(1)
                continue
            file_path = folder / f'{safe_title}_{int(time.time())}.mp4'
            print('Tiêu đề TikTok:', title)
            print('Video URL:', video_url)
            print('Lưu file:', file_path)
            video_res = requests.get(video_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/123 Safari/537.36'}, stream=True, timeout=60)
            if video_res.status_code != 200:
                print('Tải video lỗi HTTP:', video_res.status_code)
                wait(1)
                continue
            with open(file_path, 'wb') as f:
                for chunk in video_res.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            if not file_path.exists() or file_path.stat().st_size < 1000:
                print('File tải về quá nhỏ hoặc không tồn tại.')
                wait(1)
                continue
            print('Tải xong:', file_path)
            return (file_path, title)
        except Exception as e:
            print('Lỗi tải TikTok:', e)
            wait(1)
    return (None, None)


def get_video_duration(video_path):
    cmd = [
        FFPROBE_EXE,
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f'Không đọc được duration video: {result.stderr}')
    duration = float(result.stdout.strip())
    if duration <= 0:
        raise Exception('Duration video không hợp lệ.')
    return duration


def has_audio_stream(video_path):
    cmd = [
        FFPROBE_EXE,
        '-v', 'error',
        '-select_streams', 'a:0',
        '-show_entries', 'stream=index',
        '-of', 'csv=p=0',
        str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0 and bool(result.stdout.strip())


def shuffle_video_segments(total_duration):
    clip_durations = [2.25, 2.20, 2.20, 2.15, 2.20, 2.15]
    positions = [0.03, 0.20, 0.38, 0.56, 0.74, 0.90]
    segments = []

    for index, percent in enumerate(positions):
        duration = min(clip_durations[index], total_duration)
        max_start = max(0.0, total_duration - duration)
        start = min(total_duration * percent, max_start)
        segments.append({'start': start, 'duration': duration})

    random.shuffle(segments)

    for index, segment in enumerate(segments):
        wanted = clip_durations[index]
        remaining = max(0.1, total_duration - segment['start'])
        segment['duration'] = min(wanted, remaining)

    return segments


def build_slow_zoom_filter(index, duration):
    """Zoom trung bình, chậm, mượt. Xen kẽ zoom in/out; clip 5 có pan nhẹ."""
    base = (
        f'scale={EDIT_WIDTH}:{EDIT_HEIGHT}:force_original_aspect_ratio=increase,'
        f'crop={EDIT_WIDTH}:{EDIT_HEIGHT},'
        'setsar=1,'
        f'fps={EDIT_FPS}'
    )

    if index == 0:
        scale = f"1.03+0.10*t/{duration}"
        crop_x = '(iw-ow)/2'
    elif index == 1:
        scale = f"1.13-0.10*t/{duration}"
        crop_x = '(iw-ow)/2'
    elif index == 2:
        scale = f"1.04+0.08*t/{duration}"
        crop_x = '(iw-ow)/2'
    elif index == 3:
        scale = f"1.12-0.08*t/{duration}"
        crop_x = '(iw-ow)/2'
    elif index == 4:
        scale = f"1.04+0.08*t/{duration}"
        crop_x = f"(iw-ow)*(0.30+0.40*t/{duration})"
    else:
        scale = f"1.03+0.08*t/{duration}"
        crop_x = '(iw-ow)/2'

    return (
        f"{base},"
        f"scale=w='trunc({EDIT_WIDTH}*({scale})/2)*2':"
        f"h='trunc({EDIT_HEIGHT}*({scale})/2)*2':eval=frame,"
        f"crop={EDIT_WIDTH}:{EDIT_HEIGHT}:x='{crop_x}':y='(ih-oh)/2',"
        'setsar=1'
    )


def edit_video_for_shopee(input_path):
    input_path = Path(input_path)
    output_path = input_path.parent / f'{input_path.stem}_edited.mp4'

    print('=' * 60)
    print('AUTO EDIT VIDEO TRƯỚC KHI ĐẨY LÊN SHOPEE')
    print('Input :', input_path)
    print('Output:', output_path)
    print('=' * 60)

    if not Path(FFMPEG_EXE).exists():
        raise Exception(f'Không tìm thấy FFmpeg: {FFMPEG_EXE}')
    if not Path(FFPROBE_EXE).exists():
        raise Exception(f'Không tìm thấy FFprobe: {FFPROBE_EXE}')

    total_duration = get_video_duration(input_path)
    has_audio = has_audio_stream(input_path)
    segments = shuffle_video_segments(total_duration)

    for i, seg in enumerate(segments, 1):
        print(f'Clip {i}: {seg["start"]:.2f}s -> {seg["start"] + seg["duration"]:.2f}s ({seg["duration"]:.2f}s)')

    transition_pool = ['fade', 'dissolve', 'slideleft', 'slideright', 'circleopen']
    transitions = []
    previous = None
    for _ in range(len(segments) - 1):
        choices = [x for x in transition_pool if x != previous] or transition_pool
        selected = random.choice(choices)
        transitions.append(selected)
        previous = selected

    cmd = [FFMPEG_EXE, '-y', '-i', str(input_path)]

    for seg in segments[1:]:
        cmd.extend([
            '-ss', f'{seg["start"]:.3f}',
            '-t', f'{seg["duration"]:.3f}',
            '-i', str(input_path),
        ])

    filters = []
    first = segments[0]
    filters.append(
        f'[0:v]'
        f'trim=start={first["start"]}:duration={first["duration"]},'
        f'setpts=PTS-STARTPTS,'
        f'{build_slow_zoom_filter(0, first["duration"])}'
        f'[v0]'
    )

    for index in range(1, len(segments)):
        seg = segments[index]
        filters.append(
            f'[{index}:v]'
            f'{build_slow_zoom_filter(index, seg["duration"])},'
            f'setpts=PTS-STARTPTS'
            f'[v{index}]'
        )

    accumulated = segments[0]['duration']
    previous_label = 'v0'

    for index in range(1, len(segments)):
        offset = accumulated - EDIT_TRANSITION_DURATION * index
        out_label = 'vout' if index == len(segments) - 1 else f'vx{index}'
        transition = transitions[index - 1]
        filters.append(
            f'[{previous_label}][v{index}]'
            f'xfade=transition={transition}:'
            f'duration={EDIT_TRANSITION_DURATION}:'
            f'offset={offset}'
            f'[{out_label}]'
        )
        accumulated += segments[index]['duration']
        previous_label = out_label

    cmd.extend([
        '-filter_complex', ';'.join(filters),
        '-map', '[vout]',
    ])

    if has_audio:
        cmd.extend(['-map', '0:a:0?'])

    cmd.extend([
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-crf', '21',
        '-pix_fmt', 'yuv420p',
        '-r', str(EDIT_FPS),
    ])

    if has_audio:
        cmd.extend(['-c:a', 'copy'])

    cmd.extend([
        '-t', str(min(EDIT_TARGET_DURATION, total_duration)),
        '-movflags', '+faststart',
        str(output_path),
    ])

    print('Transitions:', transitions)
    print('Bắt đầu FFmpeg edit...')
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(result.stderr)
        raise Exception('Edit video bằng FFmpeg thất bại.')

    if not output_path.exists() or output_path.stat().st_size < 1000:
        raise Exception('Video edit không được tạo hoặc file quá nhỏ.')

    print('EDIT VIDEO THÀNH CÔNG:', output_path)
    return output_path

def push_video_to_phone(device_id, video_path):
    print('Đẩy video vào điện thoại...')
    adb('shell mkdir -p "/sdcard/DCIM/Camera"', device_id)
    adb(f'shell rm -f "{PHONE_VIDEO_PATH}"', device_id)
    adb(f'push "{video_path}" "{PHONE_VIDEO_PATH}"', device_id)
    adb(f'shell touch "{PHONE_VIDEO_PATH}"', device_id)
    adb(f'shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{PHONE_VIDEO_PATH}', device_id)
    adb('shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/DCIM/Camera', device_id)
    wait(3)

def delete_video_from_phone(device_id):
    print('Xóa video trên điện thoại...')
    adb(f'shell rm -f "{PHONE_VIDEO_PATH}"', device_id)
    adb(f'shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{PHONE_VIDEO_PATH}', device_id)
    wait(0.5)

def delete_video_from_pc(video_path):
    print('Xóa video trên máy tính...')
    try:
        if video_path:
            Path(video_path).unlink(missing_ok=True)
            print('Đã xóa video PC:', video_path)
    except Exception as e:
        print('Không xóa được video PC:', e)

def find_gallery_video_cells(d):
    """
    Tìm các ô video đang hiển thị trong màn Bộ sưu tập.
    Dựa vào XML:
    - tab area nằm trên y ~ 236-360
    - grid video bắt đầu dưới y ~ 363
    - item video nằm trong RecyclerView / FrameLayout
    """
    candidates = []
    xpaths = ['//*[@resource-id="com.shopee.vn:id/viewpager_gallery"]//*[@clickable="true"]', '//*[@resource-id="com.shopee.vn:id/viewpager_gallery"]//android.widget.FrameLayout', '//*[@resource-id="com.shopee.vn:id/viewpager_gallery"]//android.view.ViewGroup', '//*[@class="android.widget.FrameLayout" and @visible-to-user="true"]']
    seen = set()
    for xp in xpaths:
        try:
            items = d.xpath(xp).all()
        except Exception:
            continue
        for item in items:
            try:
                info = item.info or {}
                b = info.get('bounds')
                if isinstance(b, dict):
                    left = int(b.get('left', 0))
                    top = int(b.get('top', 0))
                    right = int(b.get('right', 0))
                    bottom = int(b.get('bottom', 0))
                else:
                    parsed = parse_bounds(str(b))
                    if not parsed:
                        continue
                    left, top, right, bottom = parsed
                width = right - left
                height = bottom - top
                if top < 360:
                    continue
                if bottom > 2100:
                    continue
                if width < 120 or height < 120:
                    continue
                if width > 700 or height > 700:
                    continue
                key = (left, top, right, bottom)
                if key in seen:
                    continue
                seen.add(key)
                candidates.append({'item': item, 'bounds': key, 'area': width * height, 'top': top, 'left': left})
            except Exception:
                continue
    candidates.sort(key=lambda x: (x['top'], x['left'], -x['area']))
    print('Gallery video candidates:')
    for i, c in enumerate(candidates[:20], 1):
        print(i, c['bounds'], 'area=', c['area'])
    return candidates

def click_first_gallery_video_checkbox(d):
    """
    Tick chọn clip bằng vòng tròn checkbox ở góc phải trên của ô video.
    Không bấm vào giữa video vì sẽ mở preview.
    Đây không phải tọa độ cố định:
    - Lấy bounds ô video từ XML runtime.
    - Tính điểm checkbox theo bounds của ô đó.
    """
    print('Tick chọn clip bằng checkbox trong ô video...')
    candidates = find_gallery_video_cells(d)
    if not candidates:
        raise Exception('Không tìm thấy ô video trong gallery để tick checkbox.')
    chosen = candidates[0]
    left, top, right, bottom = chosen['bounds']
    x = right - max(25, int((right - left) * 0.12))
    y = top + max(25, int((bottom - top) * 0.12))
    print('Chosen video cell:', chosen['bounds'], 'checkbox dynamic point:', (x, y))
    d.click(x, y)
    wait(8)
    return True

def click_first_gallery_video(d):
    """
    Fallback cũ: bấm giữa ô video.
    Chỉ dùng khi thật sự cần preview.
    Luồng OneClip KHÔNG dùng hàm này nữa.
    """
    print('Chọn video đầu tiên bằng giữa ô video...')
    candidates = find_gallery_video_cells(d)
    if not candidates:
        raise Exception('Không tìm thấy ô video trong gallery. Kiểm tra XML để sửa find_gallery_video_cells().')
    chosen = candidates[0]
    print('Chosen gallery video:', chosen['bounds'])
    click_dynamic_center(d, chosen['item'], 'first_gallery_video', after_click=2)
    return True

def open_shopee(d):
    print('Mở Shopee...')
    d.app_start(SHOPEE_PACKAGE)
    wait(3)
    close_home_popups(d)

def close_home_popups(d):
    print('Kiểm tra popup Home...')
    for i in range(3):
        clicked = click_ui(d, 'home_popup_close', timeout=2, after_click=1, optional=True)
        if not clicked:
            break

def restart_shopee(device_id, d):
    print('Khởi động lại Shopee...')
    adb(f'shell am force-stop {SHOPEE_PACKAGE}', device_id)
    wait(3)
    d.app_start(SHOPEE_PACKAGE)
    wait(3)
    close_home_popups(d)

def go_to_live_video(d):
    print('Vào Live & Video...')
    close_home_popups(d)
    click_ui(d, 'live_video_tab', timeout=15, after_click=4)
    return True

def open_create_video(d):
    print('Bấm dấu + / tạo video...')
    click_ui(d, 'create_plus', timeout=15, after_click=3)
    return True

def open_gallery(d):
    print('Mở thư viện...')
    click_ui(d, 'gallery_entrance', timeout=15, after_click=4)
    return True

def is_preview_screen(d):
    """
    Màn preview là màn có video toàn màn hình và nút Tiếp theo phía dưới.
    Nếu rơi vào màn này nghĩa là đã bấm nhầm vào giữa clip.
    """
    try:
        if d(textContains='Tiếp theo').exists(timeout=0):
            if d(resourceId='com.shopee.vn:id/view_pager').exists(timeout=0):
                return True
            if d(resourceId='com.shopee.vn:id/video_container').exists(timeout=0):
                return True
    except Exception:
        pass
    return False

def find_oneclip_effect_items(d):
    """
    Fix theo XML thực tế:
    Danh sách mẫu/hiệu ứng nằm trong RecyclerView:
        resource-id="com.shopee.vn:id/rv_template_switch"

    Mỗi item hiệu ứng là LinearLayout clickable=true, bounds ví dụ:
        [37,1816][290,2223]
        [324,1816][577,2223]
        [611,1816][864,2223]

    Code cũ lọc bottom > 2100 nên loại hết item. Bản này lấy đúng item con
    trong rv_template_switch và bỏ item đầu tiên "Chỉnh sửa" nếu còn item khác.
    """
    candidates = []
    seen = set()
    xpaths = ['//*[@resource-id="com.shopee.vn:id/rv_template_switch"]//android.widget.LinearLayout[@clickable="true"]', '//*[@resource-id="com.shopee.vn:id/rv_template_switch"]//*[@clickable="true"]', '//*[@resource-id="com.shopee.vn:id/rv_template_switch"]//android.widget.LinearLayout']
    for xp in xpaths:
        try:
            items = d.xpath(xp).all()
        except Exception:
            continue
        for item in items:
            try:
                info = item.info or {}
                b = info.get('bounds')
                if isinstance(b, dict):
                    left = int(b.get('left', 0))
                    top = int(b.get('top', 0))
                    right = int(b.get('right', 0))
                    bottom = int(b.get('bottom', 0))
                else:
                    parsed = parse_bounds(str(b))
                    if not parsed:
                        continue
                    left, top, right, bottom = parsed
                width = right - left
                height = bottom - top
                if top < 1700:
                    continue
                if bottom > 2265:
                    continue
                if width < 120 or height < 250:
                    continue
                key = (left, top, right, bottom)
                if key in seen:
                    continue
                seen.add(key)
                text = ''
                try:
                    text = info.get('text') or ''
                except Exception:
                    pass
                candidates.append({'item': item, 'bounds': key, 'top': top, 'left': left, 'area': width * height, 'text': text})
            except Exception:
                continue
    candidates.sort(key=lambda x: (x['top'], x['left']))
    print('OneClip template/effect candidates:')
    for i, c in enumerate(candidates, 1):
        print(i, c['bounds'], 'text=', c.get('text'), 'area=', c['area'])
    return candidates

def choose_random_oneclip_effect(d):
    """
    Chọn ngẫu nhiên 1 mẫu/hiệu ứng OneClip.
    Bỏ item đầu tiên nếu nó là 'Chỉnh sửa' / template hiện tại, rồi random trong các item còn lại.
    """
    print('Chọn ngẫu nhiên 1 hiệu ứng OneClip...')
    wait(8)
    candidates = find_oneclip_effect_items(d)
    if not candidates:
        raise Exception('Không tìm thấy danh sách hiệu ứng OneClip trong rv_template_switch. Kiểm tra màn hình oneclip_effect_not_found để kiểm tra.')
    pickable = candidates[1:] if len(candidates) > 1 else candidates
    chosen = random.choice(pickable)
    print('Random effect chosen:', chosen['bounds'], 'text=', chosen.get('text'))
    click_dynamic_center(d, chosen['item'], 'random_oneclip_effect', after_click=4)
    return True

def choose_video(d):
    print('Tick chọn clip rồi nhấn OneClip...')
    click_ui(d, 'gallery_video_tab', timeout=8, after_click=2, optional=True)
    wait(1)
    click_first_gallery_video_checkbox(d)
    if is_preview_screen(d):
        raise Exception('Đã mở preview video, nghĩa là điểm tick checkbox chưa đúng. Kiểm tra ảnh/XML wrong_opened_preview_after_checkbox để chỉnh hàm click_first_gallery_video_checkbox().')
    if not click_ui(d, 'oneclip', timeout=15, after_click=3, optional=True):
        raise Exception('Đã tick clip nhưng không thấy OneClip. Kiểm tra màn hình oneclip_not_found_after_tick_clip để sửa selector OneClip.')
    choose_random_oneclip_effect(d)
    wait(8)
    click_ui(d, 'next_button', timeout=25, after_click=4)
    click_ui(d, 'next_button', timeout=12, after_click=4, optional=True)
    return True

def fill_caption(device_id, d, caption):
    print('Nhập caption từ tiêu đề TikTok...')
    print('Caption:', caption)
    caption = caption or ''
    input_ui(d, 'caption_box', caption, timeout=12)
    clicked_ok = click_ui(d, 'confirm_ok', timeout=3, after_click=1, optional=True)
    if not clicked_ok:
        press_escape(device_id, delay=1)
    return True

def open_add_product_page(d):
    print('Mở trang thêm sản phẩm...')
    click_ui(d, 'add_product_entry', timeout=20, after_click=4)
    wait_text_any(d, ['Tìm kiếm', 'Thêm sản phẩm', 'Sản phẩm'], timeout=5)
    return True

def click_top_right_product_link_icon(d):
    """
    Fix màn Thêm sản phẩm:
    Trên màn này có tab 'Tiếp thị liên kết' cũng chứa chữ 'liên kết',
    nên selector desc_contains='link/liên kết' rất dễ click nhầm vào tab.

    Icon dán link hàng loạt là icon dây xích ở góc phải trên.
    XML của màn này thường chỉ có ImageView, không có text/content-desc.
    Vì vậy lấy bounds động của ImageView nằm góc phải trên rồi click vào tâm.
    Không dùng tọa độ cố định.
    """
    print('Click icon dây xích nhập link hàng loạt ở góc phải trên...')
    candidates = []
    xpaths = ['//*[@class="android.widget.ImageView" and @visible-to-user="true"]', '//android.widget.ImageView']
    for xp in xpaths:
        try:
            items = d.xpath(xp).all()
        except Exception:
            continue
        for item in items:
            try:
                info = item.info or {}
                b = info.get('bounds')
                if isinstance(b, dict):
                    left = int(b.get('left', 0))
                    top = int(b.get('top', 0))
                    right = int(b.get('right', 0))
                    bottom = int(b.get('bottom', 0))
                else:
                    parsed = parse_bounds(str(b))
                    if not parsed:
                        continue
                    left, top, right, bottom = parsed
                width = right - left
                height = bottom - top
                if left < 880:
                    continue
                if top > 230:
                    continue
                if width < 35 or height < 35:
                    continue
                if width > 140 or height > 140:
                    continue
                candidates.append({'item': item, 'bounds': (left, top, right, bottom), 'left': left, 'top': top, 'area': width * height})
            except Exception:
                continue
    candidates.sort(key=lambda x: (x['top'], -x['left']))
    print('Top right link icon candidates:')
    for i, c in enumerate(candidates[:10], 1):
        print(i, c['bounds'], 'area=', c['area'])
    if not candidates:
        raise Exception('Không tìm thấy icon dây xích góc phải trên. Kiểm tra XML top_right_product_link_icon_not_found để chỉnh hàm click_top_right_product_link_icon().')
    chosen = candidates[0]
    print('Chosen product link icon:', chosen['bounds'])
    click_dynamic_center(d, chosen['item'], 'top_right_product_link_icon', after_click=2)
    return True

def is_link_form_open(d):
    """
    Kiểm tra đã mở màn/form nhập link hàng loạt chưa.
    """
    checks = ['Nhập liên kết', 'Liên kết sản phẩm', 'Dán liên kết', 'Nhập link', 'link sản phẩm', 'liên kết sản phẩm']
    for text in checks:
        try:
            if d(textContains=text).exists(timeout=0):
                return True
        except Exception:
            pass
    try:
        if d(className='android.widget.EditText').exists(timeout=0):
            return True
    except Exception:
        pass
    return False

def open_product_link_form(d):
    print('Mở form nhập link Shopee hàng loạt...')
    click_top_right_product_link_icon(d)
    wait(1)
    if not is_link_form_open(d):
        print('Chưa thấy form nhập link, thử click icon dây xích lần 2...')
        click_top_right_product_link_icon(d)
        wait(1)
    if not is_link_form_open(d):
        raise Exception('Click icon dây xích rồi nhưng chưa mở form nhập link. Mở screenshot/XML after_retry_click_top_right_link_icon để kiểm tra.')
    return True

def paste_shopee_links(d, links):
    print('Paste link Shopee...')
    links = [x.strip() for x in links if x and x.strip()]
    text = '\n'.join(links)
    print('Số link:', len(links))
    print(text)
    if not text:
        print('Không có link để paste.')
        return False
    input_ui(d, 'link_input', text, timeout=10)
    wait(3)
    return True

def click_import_links(d):
    print('Bấm nút Nhập...')
    click_ui(d, 'import_button', timeout=15, after_click=5)
    return True

def wait_product_list_loaded(d, timeout=30):
    print('Đợi danh sách sản phẩm load...')
    start = time.time()
    while time.time() - start < timeout:
        if wait_text_any(d, ['Chọn tất cả', 'Thêm(', 'Tỷ lệ hoa hồng'], timeout=1):
            print('Đã thấy danh sách sản phẩm.')
            return True
        wait(0.5)
    print('Chưa thấy danh sách sản phẩm.')
    return False

def select_all_products(d):
    print('Bấm Chọn tất cả...')
    click_ui(d, 'select_all', timeout=15, after_click=3)
    return True

def click_add_selected_products(d):
    print('Bấm Thêm(x)...')
    click_ui(d, 'add_selected', timeout=15, after_click=4)
    return True

def add_products_by_links(d, shopee_links):
    if not shopee_links:
        print('Không có link Shopee.')
        return False
    if not open_add_product_page(d):
        return False
    if not open_product_link_form(d):
        return False
    if not paste_shopee_links(d, shopee_links):
        return False
    if not click_import_links(d):
        return False
    if not wait_product_list_loaded(d, timeout=30):
        return False
    if not select_all_products(d):
        return False
    if not click_add_selected_products(d):
        return False
    return True

def close_whatsapp_share_popup(d):
    print('Kiểm tra popup chia sẻ WhatsApp...')
    try:
        if wait_text_any(d, ['WhatsApp', 'Hủy', 'Cancel'], timeout=3):
            click_ui(d, 'cancel_popup', timeout=5, after_click=1, optional=True)
            print('Đã xử lý popup.')
            return True
    except Exception as e:
        print('Không xử lý popup:', e)
    return False

def publish_video(d):
    print('Bấm Đăng...')
    click_ui(d, 'post_button', timeout=25, after_click=5)
    print('Đã bấm Đăng.')
    return True

def skip_job(device_id, d, video_path, reason, original_video_path=None):
    print('=' * 60)
    print('BỎ QUA JOB')
    print('Lý do:', reason)
    print('=' * 60)
    try:
        delete_video_from_phone(device_id)
    except Exception as e:
        print('Không xóa được video trên điện thoại:', e)
    try:
        if video_path:
            delete_video_from_pc(video_path)
        if original_video_path and Path(original_video_path) != Path(video_path or ''):
            delete_video_from_pc(original_video_path)
    except Exception as e:
        print('Không xóa được video trên PC:', e)
    try:
        restart_shopee(device_id, d)
    except Exception as e:
        print('Không restart được Shopee:', e)


def process_one_job(device_id, d, job, index):
    video_path = None
    original_video_path = None
    try:
        tiktok_url = job.get('link_tiktok')
        shopee_links = job.get('shopee_links') or []

        if not tiktok_url:
            print('Job không có link_tiktok.')
            return False

        video_path, title = download_tiktok(tiktok_url, VIDEO_DIR)
        if not video_path:
            print('Không tải được video TikTok.')
            return False

        original_video_path = video_path
        caption = title or ''

        if EDIT_VIDEO_BEFORE_POST:
            print('=' * 60)
            print('BẮT ĐẦU EDIT VIDEO TRƯỚC KHI POST')
            print('=' * 60)
            video_path = edit_video_for_shopee(original_video_path)
            print('Video dùng để đăng:', video_path)

        push_video_to_phone(device_id, video_path)

        go_to_live_video(d)
        open_create_video(d)
        open_gallery(d)

        # Vẫn sử dụng OneClip như flow cũ
        choose_video(d)

        if not fill_caption(device_id, d, caption):
            skip_job(device_id, d, video_path, 'Không nhập được caption', original_video_path)
            return False

        if not add_products_by_links(d, shopee_links):
            skip_job(device_id, d, video_path, 'Không thêm được link Shopee', original_video_path)
            return False

        if PUBLISH_AFTER_ADD_PRODUCT:
            if not publish_video(d):
                skip_job(device_id, d, video_path, 'Không đăng được video', original_video_path)
                return False
            wait(1)
        else:
            print('PUBLISH_AFTER_ADD_PRODUCT = False, không bấm Đăng.')

        close_whatsapp_share_popup(d)
        delete_video_from_phone(device_id)
        delete_video_from_pc(video_path)

        if original_video_path and Path(original_video_path) != Path(video_path):
            delete_video_from_pc(original_video_path)

        print('=' * 60)
        print('HOÀN TẤT JOB')
        print('Tiêu đề:', title)
        print('=' * 60)
        return True

    except Exception as e:
        print('Lỗi job:', e)
        if STOP_ON_SELECTOR_ERROR:
            raise
        skip_job(device_id, d, video_path, 'Lỗi ngoài ý muốn hoặc selector sai', original_video_path)
        return False

def main():
    jobs = load_jobs_from_google_sheet_readonly()
    if not jobs:
        print('Không có job nào trong Google Sheet.')
        return
    device_id = get_device_id()
    if not device_id:
        return
    d = u2.connect(device_id)
    open_shopee(d)
    for index, job in enumerate(jobs, 1):
        print('=' * 60)
        print(f'BẮT ĐẦU JOB {index}/{len(jobs)}')
        print('=' * 60)
        process_one_job(device_id, d, job, index)
        wait(1)
    print('=' * 60)
    print('HOÀN TẤT TẤT CẢ JOB.')
    print('=' * 60)
if __name__ == '__main__':
    main()
