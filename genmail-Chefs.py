import aiohttp
import asyncio
import random
import string
from bs4 import BeautifulSoup

CAC_TEN_MIEN = list(set([
    "imail.edu.vn", "gddp2018.edu.vn", "naka.edu.pl", "collegewh.edu.pl",
    "mailo.edu.pl", "nik.edu.pl", "apple.edu.pl", "itmo.edu.pl",
    "mailer.edu.pl", "jakarta.io.vn", "newdelhi.in.vn", "mallo.edu.pr",
    "newdelhi.io.vn", "tempmail.io.vn", "mailer.io.vn",
    "newyork.io.vn", "dulieu.io.vn"
]))

def tao_email_ngau_nhien():
    ten = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(8, 12)))
    mien = random.choice(CAC_TEN_MIEN)
    return f"{ten}@{mien}"

async def tao_1_tai_khoan(password, stt, tong):
    try:
        email = tao_email_ngau_nhien()
        print(f"\n📨 [{stt}/{tong}] Đang tạo: {email}")
        print("⏳ Đang nhập thông tin...")

        url_form = 'https://www.fallenrookpublishing.co.uk/shop/my-account/'

        headers_get = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'vi',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        }

        # ⚠️ Mỗi email dùng session riêng
        async with aiohttp.ClientSession() as session:
            async with session.get(url_form, headers=headers_get) as resp:
                text = await resp.text()
                status = resp.status

                soup = BeautifulSoup(text, 'html.parser')
                nonce_input = soup.find("input", {"name": "woocommerce-register-nonce"})
                nonce = nonce_input['value'] if nonce_input else None

                if not nonce:
                    print(f"⚠️ Không lấy được nonce! [HTTP {status}]")
                    # with open("error_nonce_debug.html", "w", encoding="utf-8") as f:
                    #     f.write(text)
                    # print("🛠 Đã lưu HTML lỗi vào file: error_nonce_debug.html")
                    return None

            data = {
                'email': email,
                'password': password,
                'wc_order_attribution_source_type': 'typein',
                'wc_order_attribution_referrer': '(none)',
                'wc_order_attribution_utm_campaign': '(none)',
                'wc_order_attribution_utm_source': '(direct)',
                'wc_order_attribution_utm_medium': '(none)',
                'wc_order_attribution_utm_content': '(none)',
                'wc_order_attribution_utm_id': '(none)',
                'wc_order_attribution_utm_term': '(none)',
                'wc_order_attribution_utm_source_platform': '(none)',
                'wc_order_attribution_utm_creative_format': '(none)',
                'wc_order_attribution_utm_marketing_tactic': '(none)',
                'wc_order_attribution_session_entry': url_form,
                'wc_order_attribution_session_start_time': '2025-09-06 03:04:47',
                'wc_order_attribution_session_pages': '1',
                'wc_order_attribution_session_count': '1',
                'wc_order_attribution_user_agent': headers_get['user-agent'],
                'woocommerce-register-nonce': nonce,
                '_wp_http_referer': '/shop/my-account/',
                'register': 'Register',
            }

            headers_post = {
                'accept': headers_get['accept'],
                'accept-language': headers_get['accept-language'],
                'cache-control': 'max-age=0',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.fallenrookpublishing.co.uk',
                'priority': headers_get['priority'],
                'referer': url_form,
                'sec-ch-ua': headers_get['sec-ch-ua'],
                'sec-ch-ua-mobile': headers_get['sec-ch-ua-mobile'],
                'sec-ch-ua-platform': headers_get['sec-ch-ua-platform'],
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': headers_get['user-agent'],
            }

            async with session.post(url_form, headers=headers_post, data=data) as resp:
                text = await resp.text()
                if "My account" in text or "Logout" in text:
                    print(f"✅ Tạo thành công: {email}")
                    return email
                else:
                    print(f"❌ Tạo thất bại: {email}")
                    return None

    except Exception as e:
        print(f"🚫 Lỗi tạo tài khoản [{stt}/{tong}]: {e}")
        return None

async def main():
    try:
        so_luong = int(input("Bạn muốn tạo bao nhiêu tài khoản? "))
    except:
        print("⚠️ Vui lòng nhập số hợp lệ.")
        return

    passwordmail = "Abcxyz@123456@"
    emails_thanh_cong = []

    for i in range(1, so_luong + 1):
        email = await tao_1_tai_khoan(passwordmail, i, so_luong)
        if email:
            emails_thanh_cong.append(email)
        print(f"📊 Tiến trình: {i}/{so_luong} đã hoàn thành.")
        delay = random.uniform(2.5, 5.0)
        print(f"⏱️ Chờ {delay:.2f} giây...\n")
        await asyncio.sleep(delay)

    with open("danh_sach_email.txt", "w", encoding="utf-8") as f:
        for email in emails_thanh_cong:
            f.write(f"\"{email}\"\n")

    print(f"\n📁 Đã lưu {len(emails_thanh_cong)} tài khoản vào file 'danh_sach_email.txt'")


if __name__ == "__main__":
    asyncio.run(main())
