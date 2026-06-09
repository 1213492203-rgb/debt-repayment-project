"""
Chengjubao (devlg.com) Profile & Service Auto-Filler
=====================================================
Usage: python -X utf8 scripts/fill_chengjubao.py [--dry-run]
"""

import asyncio
import sys
from pathlib import Path

# Fix Windows GBK encoding for emoji
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SESSION_DIR = PROJECT_ROOT / ".playwright-sessions" / "chengjubao"
SESSION_DIR.mkdir(parents=True, exist_ok=True)

# 程聚宝 Profile 数据
PROFILE = {
    "nickname": "全栈开发者 | AI工具流专家",
    "bio": (
        "5年全栈开发经验，精通 React/Next.js/Vue/Python 技术栈。\n"
        "借助 AI 辅助开发工具，效率可达传统开发的 3-5 倍，因此报价比市场低 30-50%。\n"
        "交付准时率 100%，提供 1 个月免费维护，工作日 2 小时内响应。\n"
        "远程全职接单，期待长期合作。\n\n"
        "作品链接：\n"
        "- AI周报生成器：https://weekly-report-ai.pages.dev/\n"
        "- GitHub：https://github.com/1213492203-rgb"
    ),
    "skills": ["React", "Next.js", "TypeScript", "Python", "小程序", "数据可视化", "AI应用开发"],
}

# 程聚宝服务列表
SERVICES = [
    {"name": "企业官网/落地页开发", "price": "500-1500元", "delivery": "1-3天",
     "desc": "响应式设计，SEO优化，含联系表单。AI工具提效，比市场价低30-50%。"},
    {"name": "微信小程序开发", "price": "1000-3000元", "delivery": "3-7天",
     "desc": "支付集成+用户系统+管理后台，完整交付+1月免费维护。"},
    {"name": "后台管理系统", "price": "2000-5000元", "delivery": "5-14天",
     "desc": "数据面板+CRUD+权限管理，React/Next.js 技术栈。"},
    {"name": "Python自动化脚本", "price": "300-1000元", "delivery": "1-2天",
     "desc": "爬虫/数据处理/自动报表，含详细注释和README。"},
    {"name": "AI应用/工具开发", "price": "800-3000元", "delivery": "2-7天",
     "desc": "ChatGPT接入/智能客服/自动化工作流，提供完整解决方案。"},
]


def print_banner():
    print("=" * 60)
    print("  程聚宝 Profile & Service Auto-Filler")
    print("  devlg.com 资料填写 + 服务发布")
    print("=" * 60)


async def wait_for_login(page):
    """等待用户手动登录程聚宝"""
    print("\n⏳ 请在浏览器中登录程聚宝 (devlg.com)...")
    print("   如果需要短信验证码，请手动输入")
    try:
        await page.wait_for_url("**/user**|**/dashboard**|**/home**", timeout=300000)
        print("✅ 检测到登录成功！")
    except Exception:
        print("⚠️  未检测到登录跳转，请确认是否已登录")
        input("   按 Enter 继续（已登录的话）...")


async def fill_profile(page):
    """填写个人资料"""
    print("\n📝 填写个人资料...")

    # 点击个人设置/Profile 页面
    profile_links = await page.query_selector_all(
        'a[href*="profile"], a[href*="settings"], a[href*="user"]'
    )
    if profile_links:
        await profile_links[0].click()
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(1)

    # 尝试填写昵称
    name_inputs = await page.query_selector_all(
        'input[name*="name"], input[placeholder*="昵称"], input[placeholder*="姓名"]'
    )
    if name_inputs:
        await name_inputs[0].fill(PROFILE["nickname"])
        print(f"   ✅ 昵称已填写: {PROFILE['nickname']}")
    else:
        print("   ⚠️ 未找到昵称输入框（可能已填写或UI不同）")

    # 尝试填写简介
    bio_textareas = await page.query_selector_all(
        'textarea[name*="bio"], textarea[placeholder*="简介"], textarea[name*="intro"]'
    )
    if bio_textareas:
        await bio_textareas[0].fill(PROFILE["bio"])
        print(f"   ✅ 简介已填写")
    else:
        print("   ⚠️ 未找到简介输入框")

    # 尝试填写技能标签
    tag_inputs = await page.query_selector_all(
        'input[class*="tag"], input[placeholder*="技能"], input[placeholder*="标签"]'
    )
    if tag_inputs:
        for skill in PROFILE["skills"]:
            await tag_inputs[0].fill(skill)
            await tag_inputs[0].press("Enter")
            await asyncio.sleep(0.3)
        print(f"   ✅ 技能标签: {', '.join(PROFILE['skills'])}")
    else:
        print("   ⚠️ 未找到技能标签输入框")

    print("   个人资料填写完毕，请在浏览器中确认并保存")


async def publish_service(page, service, index):
    """发布单个服务"""
    print(f"\n  发布服务 #{index+1}: {service['name']}")

    # 点击"发布服务"按钮
    publish_btns = await page.query_selector_all(
        'a[href*="publish"], button:has-text("发布"), a:has-text("发布服务")'
    )
    if publish_btns:
        await publish_btns[0].click()
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(1)

    # 填写服务名称
    name_inputs = await page.query_selector_all('input[name*="title"], input[name*="name"]')
    if name_inputs:
        await name_inputs[0].fill(service["name"])

    # 填写价格
    price_inputs = await page.query_selector_all('input[name*="price"], input[placeholder*="价格"]')
    if price_inputs:
        await price_inputs[0].fill(service["price"])

    # 填写描述
    desc_textareas = await page.query_selector_all('textarea[name*="desc"], textarea[name*="intro"]')
    if desc_textareas:
        await desc_textareas[0].fill(service["desc"])

    # 填写交付时间
    delivery_inputs = await page.query_selector_all(
        'input[name*="delivery"], input[placeholder*="交付"], input[placeholder*="周期"]'
    )
    if delivery_inputs:
        await delivery_inputs[0].fill(service["delivery"])

    print(f"   ✅ 服务填写完毕（请在浏览器中确认并提交）")


async def main(dry_run=False):
    print_banner()

    if dry_run:
        print("\n🔍 DRY RUN 模式 — 只打印数据\n")
        print("Profile:", PROFILE["nickname"])
        print(f"Skills: {', '.join(PROFILE['skills'])}")
        for i, s in enumerate(SERVICES):
            print(f"\n 服务{i+1}: {s['name']} | {s['price']} | {s['delivery']}")
        return

    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("❌ 需要安装 playwright: pip install playwright && playwright install chromium")
        return

    async with async_playwright() as p:
        print("\n🚀 启动浏览器...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
            viewport={"width": 1280, "height": 900},
        )
        page = context.pages[0] if context.pages else await context.new_page()

        # 打开程聚宝
        await page.goto("https://devlg.com", wait_until="networkidle", timeout=30000)

        # 检查登录
        login_btn = await page.query_selector('a[href*="login"], button:has-text("登录")')
        if login_btn:
            await wait_for_login(page)

        print("✅ 已登录程聚宝")

        # 第一步：填写 Profile
        await fill_profile(page)
        print("\n⏸️  请在浏览器中确认 Profile 并保存，然后按 Enter 继续发布服务...")
        input("   > ")

        # 第二步：逐个发布服务
        for i, service in enumerate(SERVICES):
            await publish_service(page, service, i)
            await asyncio.sleep(0.5)

        print(f"\n{'=' * 60}")
        print("  ✅ 所有服务表单已填写")
        print("  请在浏览器中一一确认并发布！")
        print(f"{'=' * 60}")

        await context.close()


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    asyncio.run(main(dry_run=dry_run))
