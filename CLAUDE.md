# CLAUDE.md — 还债项目

## 项目概要
用户欠债10万人民币，需要在6个月内用编程+AI技能还清。
项目根目录: `c:/Users/Administrator/debt-repayment-project/`

## 约束条件
- 所有平台/工具**必须免费注册**（零费用）
- 所有操作**必须在电脑浏览器完成**（不能是手机App专属）
- 我来操作用户的账号

## 项目结构
```
debt-repayment-project/
├── README.md                  # 总览
├── PROJECT_STATUS.md          # 进度追踪（每次对话先读）
├── revenue-plan.md            # 6个月10万商业计划
├── accounts-needed.md         # 需要的免费账号清单（修订版）
├── CLAUDE.md                  # 本文件 — AI自动读取
│
├── products/
│   ├── 01-weekly-report-ai/   # AI周报生成器 (Next.js 16, 含内置模板引擎)
│   ├── 02-xhs-chrome-extension/ # Chrome插件：小红书AI文案助手
│   │   └── xhs-content-helper-v1.0.0.zip  # 已打包，待分发
│   └── 03-ppt-templates/      # 3个PPT模板 + 生成脚本
│
├── marketing/
│   └── service-listings/      # 程聚宝/Fiverr接单文案
│
└── docs/
    └── research-notes.md      # 市场调研笔记
```

## 四条收入线 + 对应平台
1. AI周报生成器 SaaS → GitHub + Cloudflare Pages 部署
2. Chrome插件 → GitHub Releases 免费分发
3. 外包接单 → 程聚宝(国内) + Fiverr(国际)
4. 数字产品 → Fiverr + GitHub 销售

## 工作约定
- 先MVP再优化，不等完美
- 每次对话开始先读 PROJECT_STATUS.md
- 所有收入记录到 PROJECT_STATUS.md
- 多轨并行，不依赖单一收入源

## 当前状态 (2026-06-09 17:45)
- ✅ 4个产品代码全部完成
- ✅ 3个PPT模板 + Chrome插件 Release
- ✅ GitHub: https://github.com/1213492203-rgb/debt-repayment-project
- ✅ Cloudflare部署: https://weekly-report-ai.pages.dev/
- ✅ 5张Fiverr Gig封面图(1280x769 PNG)已生成
- ✅ 权限修复: 全局settings.json补全allow列表
- ✅ Playwright+CDP自动化脚本就绪（连桌面Chrome）
- ✅ 程聚宝自动化脚本就绪
- ⚠️ 待发布: Fiverr 5 Gig + 程聚宝 Profile/5服务
- 📋 醒后清单: 见 WAKE_UP.md

## 自动化脚本
```
scripts/
├── fill_fiverr_via_cdp.py    ★ 首选 — CDP连桌面Chrome，复用登录
├── fill_fiverr_gigs.py         备选 — 独立Chrome
├── fill_chengjubao.py          程聚宝自动填写
└── generate_gig_covers.py      5张封面图生成器
```
运行: `python -X utf8 -u scripts/<name>.py`

## 持久化配置
- Git: 1213492203-rgb, SSH push to origin
- SSH key: ~/.ssh/id_ed25519
- Cloudflare: wrangler已认证, weekly-report-ai project
- Playwright: Chromium在 ~/AppData/Local/ms-playwright/
- Chrome: C:/Program Files/Google/Chrome/Application/chrome.exe
- GITHUB_TOKEN: 每会话需提供(ghp_...)
