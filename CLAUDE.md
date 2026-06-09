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

## 当前状态 (2026-06-09 15:15)
- ✅ 4个产品代码全部完成
- ✅ 3个PPT模板(商业10页/汇报8页/简历2页) + Chrome插件.zip
- ✅ HTML单文件版(14KB)可直接浏览器打开使用
- ✅ GitHub仓库上线: https://github.com/1213492203-rgb/debt-repayment-project
- ✅ Cloudflare Pages部署: https://weekly-report-ai.pages.dev/
- ✅ Chrome插件发布: GitHub Release v1.0.0
- ✅ 程聚宝/Fiverr接单文案就绪 + 发布指南完整版
- ✅ SSH push 配置完成（绕过 HTTPS 封锁）
- ⚠️ 程聚宝 + Fiverr 需用户浏览器手动发布（内容已备好，见 marketing/publishing-guide.md）

## 技术配置（本机持久化）
- Git user: 1213492203-rgb / 1213492203-rgb@users.noreply.github.com
- Git remote: git@github.com:1213492203-rgb/debt-repayment-project.git (SSH)
- SSH key: ~/.ssh/id_ed25519 (deploy key on repo)
- Cloudflare: wrangler 已认证，project: weekly-report-ai
- GitHub PAT: 需每会话提供 (ghp_...)，或使用 GITHUB_TOKEN 环境变量
- gh CLI path: /c/Program Files/GitHub CLI/gh.exe
