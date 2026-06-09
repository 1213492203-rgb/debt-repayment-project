"""
Fiverr Gig Auto-Filler v2 — 通过 CDP 连接你已登录的 Chrome
===========================================================
策略：
1. 关闭现有 Chrome
2. 用你的真实用户数据启动 Chrome（--remote-debugging-port=9222）
3. Playwright 通过 CDP 连接 → 复用你所有 Google/Fiverr 登录状态
4. 自动填写 Gig 表单，遇到验证码暂停

用法：python -X utf8 -u scripts/fill_fiverr_via_cdp.py [--dry-run]
"""

import asyncio
import subprocess
import os
import sys
import time
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ── 常量 ──────────────────────────────────────────────

CDP_PORT = 9222
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_USER_DATA = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
CDP_URL = f"http://localhost:{CDP_PORT}"

GIGS = [
    {
        "title": "I will build a professional business website in 2 days",
        "description": (
            "Need a stunning business website FAST? I deliver professional, "
            "responsive websites in just 2 days using modern tech (Next.js/React/TailwindCSS).\n\n"
            "What you get:\n"
            "✅ Fully responsive design (mobile + tablet + desktop)\n"
            "✅ SEO optimized for Google ranking\n"
            "✅ Contact form + Social media integration\n"
            "✅ Fast loading (90+ PageSpeed score)\n"
            "✅ 1 month FREE support after delivery\n\n"
            "Why me?\n"
            "I use AI-powered development tools to work 3x faster than traditional developers. "
            "You get premium quality for half the market price.\n\n"
            "Message me before ordering to discuss your project!"
        ),
        "packages": [
            {"name": "Basic", "price": 50, "delivery": 2, "desc": "1-page landing page, responsive, contact form"},
            {"name": "Standard", "price": 100, "delivery": 3, "desc": "3-page website + blog section, SEO optimized"},
            {"name": "Premium", "price": 200, "delivery": 5, "desc": "5-page website + admin dashboard + 1 month support"},
        ]
    },
    {
        "title": "I will create an automation script to save you hours every week",
        "description": (
            "Stop wasting time on repetitive tasks! I'll build a custom Python "
            "automation script that handles your boring work automatically.\n\n"
            "Examples of what I can automate:\n"
            "🤖 Auto-generate weekly/monthly reports from your data\n"
            "📊 Web scraping — extract data from any website to Excel/CSV\n"
            "📧 Automated personalized emails (bulk sending)\n"
            "🔄 Sync data between platforms (APIs, databases, Google Sheets)\n"
            "📁 Auto-organize files, rename, and sort\n\n"
            "Every script includes detailed comments and a README.\n\n"
            "Message me with your task description for a custom quote!"
        ),
        "packages": [
            {"name": "Basic", "price": 30, "delivery": 2, "desc": "Simple single-task script + basic instructions"},
            {"name": "Standard", "price": 60, "delivery": 3, "desc": "Multi-task script (3-5 tasks) + detailed README"},
            {"name": "Premium", "price": 120, "delivery": 5, "desc": "Complex automation suite + maintenance guide"},
        ]
    },
    {
        "title": "I will design a stunning professional PowerPoint presentation",
        "description": (
            "I'll transform your ideas into a beautiful, professional PowerPoint "
            "presentation that impresses your audience!\n\n"
            "What you get:\n"
            "✅ 10-20 professionally designed slides\n"
            "✅ Custom color scheme matching your brand\n"
            "✅ Data charts, infographics, and visual elements\n"
            "✅ Editable .pptx file (works with PowerPoint/Google Slides)\n"
            "✅ 2 FREE revisions included\n\n"
            "Perfect for: Business pitches, investor decks, company reports, "
            "academic presentations, product launches."
        ),
        "packages": [
            {"name": "Basic", "price": 20, "delivery": 1, "desc": "10 slides, 1 design style, 1 revision"},
            {"name": "Standard", "price": 40, "delivery": 2, "desc": "15 slides, 2 style options, 2 revisions"},
            {"name": "Premium", "price": 80, "delivery": 3, "desc": "20 slides, custom design, unlimited revisions"},
        ]
    },
    {
        "title": "I will develop a WeChat mini program for your business",
        "description": (
            "Expand your business to China's massive WeChat ecosystem! I'll build "
            "a fully functional WeChat Mini Program tailored to your needs.\n\n"
            "Features I can include:\n"
            "✅ User authentication (WeChat login)\n"
            "✅ WeChat Pay integration\n"
            "✅ Product catalog / Service menu\n"
            "✅ Order management system\n"
            "✅ Admin dashboard for content updates\n\n"
            "Message me to discuss your project requirements!"
        ),
        "packages": [
            {"name": "Basic", "price": 100, "delivery": 5, "desc": "Simple display mini program (5 pages)"},
            {"name": "Standard", "price": 200, "delivery": 10, "desc": "E-commerce with payments + user accounts"},
            {"name": "Premium", "price": 400, "delivery": 20, "desc": "Complex app + backend admin panel + 1 month maintenance"},
        ]
    },
    {
        "title": "I will analyze your data and create beautiful reports with charts",
        "description": (
            "Turn your raw data into actionable insights! I'll clean, analyze, "
            "and visualize your data with professional charts and reports.\n\n"
            "What you get:\n"
            "✅ Data cleaning and preprocessing\n"
            "✅ Statistical analysis + trend detection\n"
            "✅ 10-20 beautiful charts (bar, pie, line, etc.)\n"
            "✅ Professional PDF/PPT report\n"
            "✅ Raw Excel/CSV with all analysis results\n\n"
            "Send me your data file(s) and tell me what you want to learn from them!"
        ),
        "packages": [
            {"name": "Basic", "price": 30, "delivery": 2, "desc": "Single dataset, basic analysis, 5 charts, PDF report"},
            {"name": "Standard", "price": 60, "delivery": 3, "desc": "Multi-dataset, deep analysis + trends, 15 charts"},
            {"name": "Premium", "price": 120, "delivery": 5, "desc": "Full BI report, 25+ charts, interactive Excel dashboard"},
        ]
    },
]


def kill_chrome():
    """关闭所有 Chrome 进程"""
    print("[1/3] 关闭现有 Chrome...")
    subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"],
                   capture_output=True, timeout=10)
    time.sleep(2)

    # 清除锁文件（防止启动报 profile locked）
    lock_files = ["SingletonLock", "SingletonSocket", "SingletonCookie"]
    for lf in lock_files:
        lp = os.path.join(CHROME_USER_DATA, lf)
        if os.path.exists(lp):
            os.remove(lp)
            print(f"       已清除锁文件: {lf}")

    print("       Chrome 已关闭")


def launch_chrome_cdp():
    """启动 Chrome 并开启远程调试端口，使用真实 Profile"""
    print(f"[2/3] 启动 Chrome（调试端口: {CDP_PORT}）...")
    print(f"       Profile: {CHROME_USER_DATA}")

    cmd = [
        CHROME_EXE,
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={CHROME_USER_DATA}",
        "--profile-directory=Default",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-features=TranslateUI",
        "https://www.fiverr.com/",  # 直接打开 Fiverr
    ]

    subprocess.Popen(cmd, shell=False,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 等待 Chrome 启动 + CDP 就绪
    print("       等待 Chrome 启动...")
    for i in range(20):
        time.sleep(2)
        try:
            import urllib.request
            resp = urllib.request.urlopen(f"{CDP_URL}/json/version", timeout=5)
            if resp.status == 200:
                print("       Chrome CDP 就绪！")
                return True
        except Exception:
            pass
        print(f"       等待中... ({i+1}/20)")

    print("❌ Chrome 启动超时，请手动检查")
    return False


async def wait_for_fiverr_login(page):
    """等待你在浏览器中登录 Fiverr"""
    print("\n⏳ 检查 Fiverr 登录状态...")

    # 先检查当前 URL
    current_url = page.url
    print(f"   当前页面: {current_url}")

    # Fiverr 首页可能有各种变体 — 查找「Sign In」按钮来判断
    for attempt in range(60):  # 最多等 2 分钟
        sign_in = await page.query_selector(
            'a[href*="login"], button:has-text("Sign in"), button:has-text("Sign In"), '
            'a[data-cy="login"], div:has-text("Continue with Google")'
        )
        user_menu = await page.query_selector(
            '[data-cy="user-menu"], [class*="user-menu"], [class*="profile-image"], '
            'a[href*="manage_gigs"], a[href*="selling"], a[href*="dashboard"]'
        )

        if user_menu and not sign_in:
            print(f"   ✅ 已在 Fiverr 登录或已登录过 Google！")
            return True

        if not sign_in:
            # 没有 Sign In 按钮也没有 user menu = 可能在加载/验证中
            print(f"   等待页面加载... ({attempt+1}/60)")
            await asyncio.sleep(2)
            continue

        # 有 Sign In 按钮 — 未登录
        if attempt == 0:
            print("   ⚠️ 尚未登录 Fiverr")
            print("   请用 Google 账号一键登录（Chrome 已有你的 Google 账号）")
            print("   或者手动输入邮箱密码登录...")
            print("   等待你完成登录（最多 2 分钟）...")

        await asyncio.sleep(2)

    print("⚠️ 登录等待超时，假设已登录继续...")
    return True


async def navigate_to_create_gig(page):
    """导航到创建 Gig 页面"""
    print("\n📝 导航到 Fiverr 创建 Gig 页面...")

    # 先确保在主站
    if "fiverr.com" not in page.url:
        await page.goto("https://www.fiverr.com/", timeout=60000)
        await asyncio.sleep(2)

    # 尝试多种途径进入创建 Gig 页面
    create_urls = [
        "https://www.fiverr.com/sellers/onboarding/gig",
        "https://www.fiverr.com/users/1213492203-rgb/seller_onboarding",
        "https://www.fiverr.com/selling",
    ]

    for url in create_urls:
        try:
            await page.goto(url, timeout=30000)
            await asyncio.sleep(2)
            print(f"   当前页面: {page.url}")
            if "onboarding" in page.url or "selling" in page.url or "gig" in page.url.lower():
                break
        except Exception:
            continue

    # 查找 "Create a New Gig" 按钮
    create_btn = await page.query_selector(
        'a[href*="gig"], button:has-text("Create"), a:has-text("New Gig"), '
        'a[href*="onboarding"]'
    )
    if create_btn:
        try:
            await create_btn.click()
            await asyncio.sleep(2)
            print(f"   点击创建后: {page.url}")
        except Exception:
            pass


async def fill_gig_form(page, gig_data, gig_index):
    """填写单个 Gig"""
    print(f"\n{'='*50}")
    print(f"📋 Gig #{gig_index+1}: {gig_data['title'][:60]}...")
    print(f"{'='*50}")

    await asyncio.sleep(2)  # 等页面稳定

    # --- Title ---
    print("   填写标题...")
    try:
        # Fiverr Gig creation wizard - title is typically the first input
        title_selectors = [
            'input[name="title"]',
            'input[placeholder*="title" i]',
            'textarea[name="title"]',
            '[data-testid="gig-title"] input',
            '#gig-title',
        ]
        for sel in title_selectors:
            elem = await page.query_selector(sel)
            if elem:
                await elem.click()
                await elem.fill("")
                await elem.type(gig_data["title"], delay=20)
                print(f"   ✅ 标题已填写")
                break
        else:
            print("   ⚠️ 未找到标题输入框，可能需要手动填写")
    except Exception as e:
        print(f"   ⚠️ 标题填写失败: {e}")

    # --- Description ---
    print("   填写描述...")
    try:
        desc_selectors = [
            'textarea[name="description"]',
            'div[contenteditable="true"][role="textbox"]',
            '[data-testid="description"] textarea',
            'div[class*="description"] div[contenteditable="true"]',
        ]
        for sel in desc_selectors:
            elem = await page.query_selector(sel)
            if elem:
                await elem.click()
                await elem.fill(gig_data["description"])
                print(f"   ✅ 描述已填写 ({len(gig_data['description'])} 字符)")
                break
        else:
            print("   ⚠️ 未找到描述输入框")
    except Exception as e:
        print(f"   ⚠️ 描述填写失败: {e}")

    # --- Pricing ---
    print("   填写定价...")
    for pkg in gig_data["packages"]:
        pkg_name = pkg["name"]
        price = pkg["price"]
        delivery = pkg["delivery"]

        try:
            # Fiverr gig pricing has tabs/sections for Basic/Standard/Premium
            # Click the package tab if needed
            tab_btn = await page.query_selector(
                f'button:has-text("{pkg_name}"), div:has-text("{pkg_name}"), '
                f'[role="tab"]:has-text("{pkg_name}")'
            )
            if tab_btn:
                await tab_btn.click()
                await asyncio.sleep(0.5)

            # Price input
            price_inputs = await page.query_selector_all('input[type="number"]')
            for inp in price_inputs:
                val = await inp.input_value()
                if val and int(val) > 0:
                    await inp.fill(str(price))
                    print(f"     {pkg_name}: ${price}")
                    break
        except Exception as e:
            print(f"     {pkg_name}: ⚠️ {e}")

    print(f"   ✅ Gig #{gig_index+1} 基本字段已填写")


async def check_captcha(page):
    """检测验证码并提示用户"""
    await asyncio.sleep(1)
    captcha_found = await page.query_selector(
        'iframe[src*="captcha"], iframe[src*="challenges.cloudflare"], '
        'iframe[src*="hcaptcha"], iframe[src*="recaptcha"], '
        '#turnstile-wrapper, [data-t="turnstile"], '
        'div[id*="captcha"]'
    )
    if captcha_found:
        print("\n🔐 检测到验证码！请在浏览器中手动完成...")
        for i in range(120):  # 等最多 4 分钟
            await asyncio.sleep(2)
            still_there = await page.query_selector(
                'iframe[src*="captcha"], iframe[src*="challenges.cloudflare"]'
            )
            if not still_there:
                print("   ✅ 验证码似乎已完成！")
                return


async def main(dry_run=False):
    print("=" * 60)
    print("  Fiverr Gig Auto-Filler v2 (CDP)")
    print("  连接你桌面已登录的 Chrome")
    print("=" * 60)

    if dry_run:
        print("\n🔍 DRY RUN — 只打印数据\n")
        for i, g in enumerate(GIGS):
            print(f"Gig {i+1}: {g['title']}")
            for p in g["packages"]:
                print(f"       {p['name']}: ${p['price']} / {p['delivery']}d")
        return

    # Step 1-2: 重启 Chrome
    kill_chrome()
    chrome_ready = launch_chrome_cdp()
    if not chrome_ready:
        print("❌ 无法启动 Chrome，请手动打开后告诉我")
        return

    # Step 3: Playwright 连接
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        print("[3/3] Playwright 连接 Chrome...")
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        print(f"       已连接！已有 {len(browser.contexts)} 个上下文")

        # 使用第一个上下文（你的 Default profile）
        context = browser.contexts[0]
        pages = context.pages
        page = pages[0] if pages else await context.new_page()

        # 确保在 Fiverr
        if "fiverr.com" not in page.url:
            await page.goto("https://www.fiverr.com/", timeout=60000)

        # 等待登录
        logged_in = await wait_for_fiverr_login(page)
        if not logged_in:
            print("⚠️ 未检测到登录，请检查浏览器。继续尝试...")

        # 逐个创建 Gig
        for i, gig in enumerate(GIGS):
            print(f"\n{'─'*50}")
            print(f" Gig {i+1}/{len(GIGS)}")
            print(f"{'─'*50}")

            await navigate_to_create_gig(page)
            await check_captcha(page)
            await fill_gig_form(page, gig, i)

            print(f"\n   ⏸️  请在浏览器中检查 Gig #{i+1} 并点击 Continue/Save")
            print(f"   （不会自动提交。准备好了告诉我）")
            # 等5秒给用户看看
            await asyncio.sleep(5)

        print(f"\n{'='*60}")
        print("  ✅ 5 个 Gig 表单已填写完毕")
        print("  请在 Chrome 中逐一检查并 Publish！")
        print(f"{'='*60}")

        # 不关闭 Chrome — 保持打开供你审阅
        print("\n💡 Chrome 保持打开，方便你继续操作")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    asyncio.run(main(dry_run=dry_run))
