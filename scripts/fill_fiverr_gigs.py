"""
Fiverr Gig Auto-Publisher -- Playwright auto form filling
========================================================
Uses Playwright persistent context to save login state.
First run requires manual login (includes CAPTCHA),
then all Gig forms are auto-filled, pausing for CAPTCHA.

Usage: python -X utf8 scripts/fill_fiverr_gigs.py [--dry-run]
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Fix Windows GBK encoding for emoji
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ── 配置 ──────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SESSION_DIR = PROJECT_ROOT / ".playwright-sessions" / "fiverr"
SESSION_DIR.mkdir(parents=True, exist_ok=True)

GIGS_FILE = PROJECT_ROOT / "marketing" / "service-listings" / "fiverr_gigs.json"

# Fiverr 5 个 Gig 的完整数据（从 publishing-guide.md 提取）
GIGS = [
    {
        "title": "I will build a professional business website in 2 days",
        "category": "Programming & Tech > Web Development",
        "tags": ["html", "css", "javascript", "react", "nextjs", "responsive"],
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
        "packages": {
            "basic": {"name": "Basic", "price": 50, "delivery_days": 2,
                       "desc": "1-page landing page, responsive, contact form"},
            "standard": {"name": "Standard", "price": 100, "delivery_days": 3,
                          "desc": "3-page website + blog section, SEO optimized"},
            "premium": {"name": "Premium", "price": 200, "delivery_days": 5,
                         "desc": "5-page website + admin dashboard + 1 month support"},
        }
    },
    {
        "title": "I will create an automation script to save you hours every week",
        "category": "Programming & Tech > Support & IT > Data Processing",
        "tags": ["python", "automation", "script", "data", "scraping", "excel"],
        "description": (
            "Stop wasting time on repetitive tasks! I'll build a custom Python "
            "automation script that handles your boring work automatically.\n\n"
            "Examples of what I can automate:\n"
            "🤖 Auto-generate weekly/monthly reports from your data\n"
            "📊 Web scraping — extract data from any website to Excel/CSV\n"
            "📧 Automated personalized emails (bulk sending)\n"
            "🔄 Sync data between platforms (APIs, databases, Google Sheets)\n"
            "📁 Auto-organize files, rename, and sort\n\n"
            "Every script includes detailed comments and a README so you understand how it works.\n\n"
            "Message me with your task description for a custom quote!"
        ),
        "packages": {
            "basic": {"name": "Basic", "price": 30, "delivery_days": 2,
                       "desc": "Simple single-task script + basic instructions"},
            "standard": {"name": "Standard", "price": 60, "delivery_days": 3,
                          "desc": "Multi-task script (3-5 tasks) + detailed README"},
            "premium": {"name": "Premium", "price": 120, "delivery_days": 5,
                         "desc": "Complex automation suite + maintenance guide"},
        }
    },
    {
        "title": "I will design a stunning professional PowerPoint presentation",
        "category": "Graphics & Design > Presentation Design",
        "tags": ["powerpoint", "presentation", "ppt", "business", "pitch-deck", "design"],
        "description": (
            "I'll transform your ideas into a beautiful, professional PowerPoint "
            "presentation that impresses your audience!\n\n"
            "What you get:\n"
            "✅ 10-20 professionally designed slides\n"
            "✅ Custom color scheme matching your brand\n"
            "✅ Data charts, infographics, and visual elements\n"
            "✅ Editable .pptx file (works with PowerPoint/Google Slides)\n"
            "✅ 2 FREE revisions included\n"
            "✅ Source file delivered — you own everything\n\n"
            "Perfect for: Business pitches, investor decks, company reports, "
            "academic presentations, product launches.\n\n"
            "Send me your content (text + data), and I'll handle the design!"
        ),
        "packages": {
            "basic": {"name": "Basic", "price": 20, "delivery_days": 1,
                       "desc": "10 slides, 1 design style, 1 revision"},
            "standard": {"name": "Standard", "price": 40, "delivery_days": 2,
                          "desc": "15 slides, 2 style options, 2 revisions"},
            "premium": {"name": "Premium", "price": 80, "delivery_days": 3,
                         "desc": "20 slides, custom design, unlimited revisions"},
        }
    },
    {
        "title": "I will develop a WeChat mini program for your business",
        "category": "Programming & Tech > Mobile App Development",
        "tags": ["wechat", "miniprogram", "weixin", "china", "ecommerce"],
        "description": (
            "Expand your business to China's massive WeChat ecosystem! I'll build "
            "a fully functional WeChat Mini Program tailored to your needs.\n\n"
            "Features I can include:\n"
            "✅ User authentication (WeChat login)\n"
            "✅ WeChat Pay integration\n"
            "✅ Product catalog / Service menu\n"
            "✅ Order management system\n"
            "✅ Admin dashboard for content updates\n"
            "✅ Push notifications via WeChat\n\n"
            "I have experience with the full WeChat ecosystem: mini programs, "
            "official accounts, and payment integration.\n\n"
            "Message me to discuss your project requirements!"
        ),
        "packages": {
            "basic": {"name": "Basic", "price": 100, "delivery_days": 5,
                       "desc": "Simple display mini program (5 pages)"},
            "standard": {"name": "Standard", "price": 200, "delivery_days": 10,
                          "desc": "E-commerce with payments + user accounts"},
            "premium": {"name": "Premium", "price": 400, "delivery_days": 20,
                         "desc": "Complex app + backend admin panel + 1 month maintenance"},
        }
    },
    {
        "title": "I will analyze your data and create beautiful reports with charts",
        "category": "Programming & Tech > Data Analysis & Reports",
        "tags": ["data-analysis", "excel", "python", "reports", "charts", "statistics"],
        "description": (
            "Turn your raw data into actionable insights! I'll clean, analyze, "
            "and visualize your data with professional charts and reports.\n\n"
            "What you get:\n"
            "✅ Data cleaning and preprocessing\n"
            "✅ Statistical analysis + trend detection\n"
            "✅ 10-20 beautiful charts (bar, pie, line, etc.)\n"
            "✅ Professional PDF/PPT report\n"
            "✅ Raw Excel/CSV with all analysis results\n\n"
            "Tools I use: Python (Pandas, Matplotlib), Excel, and AI-powered analysis tools.\n\n"
            "Send me your data file(s) and tell me what you want to learn from them!"
        ),
        "packages": {
            "basic": {"name": "Basic", "price": 30, "delivery_days": 2,
                       "desc": "Single dataset, basic analysis, 5 charts, PDF report"},
            "standard": {"name": "Standard", "price": 60, "delivery_days": 3,
                          "desc": "Multi-dataset, deep analysis + trends, 15 charts"},
            "premium": {"name": "Premium", "price": 120, "delivery_days": 5,
                         "desc": "Full BI report, 25+ charts, interactive Excel dashboard"},
        }
    },
]


def print_banner():
    print("=" * 60)
    print("  Fiverr Gig Auto-Publisher")
    print("  自动填写并发布 Fiverr Gig（表单部分）")
    print("  人机验证时会暂停等待你点击")
    print("=" * 60)


async def wait_for_login(page):
    """等待用户手动登录 Fiverr（处理 CAPTCHA）"""
    print("\n⏳ 请在浏览器中登录 Fiverr...")
    print("   如果需要验证码/人机验证，请你手动完成")
    print("   登录成功后脚本会自动继续...")

    # 等待跳转到 dashboard 或 seller 页面（登录成功的标志）
    try:
        await page.wait_for_url(
            "**/users/settings**|**/seller_dashboard**|**/manage_gigs**",
            timeout=300000  # 5分钟超时
        )
        print("✅ 检测到登录成功！")
        return True
    except Exception:
        print("⚠️  未检测到登录跳转，请确认是否已登录")
        input("   按 Enter 继续（已登录的话）...")
        return True


async def navigate_to_create_gig(page):
    """导航到 Fiverr 创建 Gig 页面"""
    print("\n📝 导航到创建 Gig 页面...")

    # Fiverr "Create a New Gig" 页面
    create_url = "https://www.fiverr.com/sellers/onboarding/gig"
    await page.goto(create_url, wait_until="networkidle", timeout=30000)

    # 如果被重定向到登录页，说明 session 过期
    if "login" in page.url:
        print("   ⚠️ Session 已过期，需要重新登录")
        await wait_for_login(page)
        await page.goto(create_url, wait_until="networkidle", timeout=30000)

    print(f"   当前页面: {page.url}")


async def fill_gig_form(page, gig_data, gig_index):
    """填写单个 Gig 的表单"""
    print(f"\n{'=' * 50}")
    print(f"📋 Gig #{gig_index + 1}: {gig_data['title'][:60]}...")
    print(f"{'=' * 50}")

    try:
        # === Title ===
        print("   填写标题...")
        title_input = await page.wait_for_selector(
            'input[name="title"], input[placeholder*="title"], #gig_title',
            timeout=10000
        )
        if title_input:
            await title_input.fill(gig_data["title"])

        # === Category ===
        print("   选择分类...")
        # Fiverr 的分类通常用下拉框/搜索选择器
        # 具体选择器因 Fiverr UI 版本而异
        category_selectors = [
            'div[class*="category"] input',
            'input[placeholder*="category"]',
            '#category-selector',
        ]
        for sel in category_selectors:
            elem = await page.query_selector(sel)
            if elem:
                await elem.click()
                await page.keyboard.type(gig_data["category"])
                await page.keyboard.press("Enter")
                await asyncio.sleep(1)
                break

        # === Tags ===
        print("   填写标签...")
        tag_input = await page.query_selector(
            'input[placeholder*="tag"], input[name*="tag"], div[class*="tag"] input'
        )
        if tag_input:
            for tag in gig_data["tags"]:
                await tag_input.fill(tag)
                await tag_input.press("Enter")
                await asyncio.sleep(0.3)

        # === Description ===
        print("   填写描述...")
        desc_textarea = await page.query_selector(
            'textarea[name="description"], textarea[placeholder*="description"], #description'
        )
        if desc_textarea:
            await desc_textarea.fill(gig_data["description"])

        # === Packages / Pricing ===
        print("   设置定价套餐...")
        packages = gig_data["packages"]
        for pkg_key in ["basic", "standard", "premium"]:
            pkg = packages[pkg_key]
            print(f"     {pkg['name']}: ${pkg['price']}")

            # 查找价格输入框（Fiverr 使用三个盒子：Basic/Standard/Premium）
            # 具体的 selector 需要根据 Fiverr 实际 HTML 调整
            price_input = await page.query_selector(
                f'input[placeholder*="price"] >> nth={list(packages.keys()).index(pkg_key)}'
            )
            if not price_input:
                # 尝试按 name 找
                price_input = await page.query_selector(
                    f'input[name*="{pkg_key}"][type="number"]'
                )
            if price_input:
                await price_input.fill(str(pkg["price"]))

        print(f"   ✅ Gig #{gig_index + 1} 表单填写完成")
        return True

    except Exception as e:
        print(f"   ⚠️ 表单填写出错: {e}")
        print("   可能 Fiverr UI 有变化，请手动继续")
        return False


async def wait_for_user_verification(page):
    """检测是否需要人机验证，暂停等用户处理"""
    # 检测常见的验证码/CAPTCHA 元素
    captcha_selectors = [
        'iframe[src*="captcha"]',
        'iframe[src*="hcaptcha"]',
        'iframe[src*="recaptcha"]',
        'div[class*="captcha"]',
        'div[id*="captcha"]',
        '#turnstile-wrapper',
        '[data-t="turnstile"]',
    ]

    for selector in captcha_selectors:
        elem = await page.query_selector(selector)
        if elem:
            print("\n🔐 检测到人机验证！请手动完成验证...")
            print("   完成验证后，脚本会自动继续")
            # 等待验证元素消失（验证成功）
            try:
                await page.wait_for_selector(
                    selector, state="detached", timeout=300000
                )
                print("   ✅ 验证完成！")
                return True
            except Exception:
                print("   ⚠️ 验证等待超时，请检查")
                return False

    # 也检测 Turnstile（Cloudflare，Fiverr 常用）
    try:
        turnstile = await page.query_selector(
            'iframe[src*="challenges.cloudflare.com"]'
        )
        if turnstile:
            print("\n🔐 检测到 Cloudflare 验证！请手动完成...")
            await page.wait_for_selector(
                'iframe[src*="challenges.cloudflare.com"]',
                state="detached", timeout=300000
            )
            print("   ✅ 验证完成！")
    except Exception:
        pass

    return True


async def main(dry_run=False):
    print_banner()

    if dry_run:
        print("\n🔍 DRY RUN 模式 — 只打印数据，不实际操作\n")
        for i, gig in enumerate(GIGS):
            print(f"Gig #{i+1}: {gig['title']}")
            print(f"  Category: {gig['category']}")
            print(f"  Tags: {', '.join(gig['tags'])}")
            print(f"  Packages: {list(gig['packages'].keys())}")
            print()
        return

    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("❌ 需要安装 playwright: pip install playwright && playwright install chromium")
        return

    async with async_playwright() as p:
        # 使用持久化上下文 — 登录状态会被保存
        print("\n🚀 启动浏览器（非隐身模式，保留登录状态）...")

        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=False,  # 显示浏览器，方便你看到并操作
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
            viewport={"width": 1280, "height": 900},
        )

        page = context.pages[0] if context.pages else await context.new_page()

        # 检查是否已登录
        print("\n🔍 检查 Fiverr 登录状态...")
        await page.goto("https://www.fiverr.com/", wait_until="networkidle", timeout=30000)

        # 判断登录状态：如果页面有 "Sign In" 按钮，则未登录
        sign_in_btn = await page.query_selector('a[href*="login"], button:has-text("Sign in"), button:has-text("Sign In")')
        if sign_in_btn:
            print("   未登录，需要先登录")
            await page.goto("https://www.fiverr.com/login", wait_until="networkidle", timeout=30000)
            await wait_for_login(page)

        print("   ✅ 已登录 Fiverr")

        # 逐个创建 Gig
        for i, gig in enumerate(GIGS):
            print(f"\n{'─' * 50}")
            print(f" 开始处理 Gig {i+1}/{len(GIGS)}")
            print(f"{'─' * 50}")

            await navigate_to_create_gig(page)
            await wait_for_user_verification(page)
            await fill_gig_form(page, gig, i)

            # ⚠️ 不自动提交！让用户审核后再点击
            print(f"\n   ⏸️  Gig #{i+1} 已填写完毕，请在浏览器中检查并点击 Publish/提交")
            print(f"   （不会自动提交，避免出错）")

            if i < len(GIGS) - 1:
                print(f"\n   准备好了按 Enter 继续下一个 Gig...")
                input("   > ")

        print(f"\n{'=' * 60}")
        print("  ✅ 所有 5 个 Gig 表单均已填写")
        print("  请在浏览器中一一确认并点击 Publish！")
        print(f"{'=' * 60}")

        await context.close()


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    asyncio.run(main(dry_run=dry_run))
