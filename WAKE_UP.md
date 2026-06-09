# ⏰ 醒后任务清单

> 休息好了？这里是睡醒后要做的事。准备好了说「**继续还债项目**」。

---

## 📊 现状：我已完成的事（你睡觉时做的）

| # | 完成项 | 说明 |
|---|--------|------|
| 1 | 权限修复 | 全局 settings.json 补全 allow 列表，下次不再弹 Yes |
| 2 | Skill 调研安装 | `playwright-automation-fill-in-form` + Playwright + Chromium |
| 3 | Fiverr CDP 脚本 | 连接你桌面 Chrome（复用登录状态），自动填 5 个 Gig |
| 4 | 程聚宝脚本 | 自动填 Profile + 5 个服务 |
| 5 | 5 张 Gig 封面图 | 1280×769 PNG，已生成在 `products/04-gig-covers/` |
| 6 | 所有代码已 push | GitHub 仓库最新 |

---

## 🎯 你要做的事（按顺序，约30分钟）

### 🥇 第一步：一键发布 Fiverr（~20分钟）

> **运行这条命令，Chrome 会自动启动（带你的所有登录状态）**

```bash
cd C:/Users/Administrator/debt-repayment-project && python -X utf8 -u scripts/fill_fiverr_via_cdp.py
```

| 脚本会做什么 | 你需要做什么 |
|-------------|------------|
| 关闭现有 Chrome | — |
| 用你的 Profile 重启 Chrome（保留所有登录） | — |
| Playwright 连上 Chrome | — |
| 打开 Fiverr | 如果弹出 Google 登录/Fiverr 登录，**点一下 Google 账号即可**（因为 Chrome 里已有你的 Google） |
| 导航到创建 Gig 页面 | — |
| 自动填标题/描述/定价 | 检查一下内容 |
| — | **上传封面图**（在 `products/04-gig-covers/` 里找对应的） |
| — | 遇到验证码点一下 |
| — | 检查无误后点 **Publish** |

> 💡 **为什么用 CDP 而不是普通脚本**：CDP 连接你桌面已有的 Chrome，所有 Google 登录/Fiverr cookie 都在，不需要重新登录。之前的脚本开了一个新的空白 Chrome，没有你的 Google 账号所以没法一键登录。

### 🥈 第二步：发布程聚宝（~10分钟）

```bash
cd C:/Users/Administrator/debt-repayment-project && python -X utf8 -u scripts/fill_chengjubao.py
```

| 脚本会做什么 | 你需要做什么 |
|-------------|------------|
| 启动 Chrome → 打开 devlg.com | 如果退出了就重新登录 |
| 自动填个人资料 | 确认保存 |
| 逐个发布 5 个服务 | 检查 → 点击发布 |

---

## 📋 脚本一览（都可用）

| 脚本 | 用途 | 命令 |
|------|------|------|
| `fill_fiverr_via_cdp.py` | ★ Fiverr — 连你桌面 Chrome | `python -X utf8 -u scripts/fill_fiverr_via_cdp.py` |
| `fill_fiverr_gigs.py` | Fiverr — 独立 Chrome（备选） | `python -X utf8 -u scripts/fill_fiverr_gigs.py` |
| `fill_chengjubao.py` | 程聚宝 Profile + 服务 | `python -X utf8 -u scripts/fill_chengjubao.py` |
| `generate_gig_covers.py` | 重新生成封面图 | `python -X utf8 scripts/generate_gig_covers.py` |

---

## 📁 封面图配对

| Gig | 封面文件 |
|-----|---------|
| 1. Build your website | `products/04-gig-covers/01-website-dev.png` |
| 2. Automation script | `products/04-gig-covers/02-automation-script.png` |
| 3. PowerPoint design | `products/04-gig-covers/03-ppt-design.png` |
| 4. WeChat mini program | `products/04-gig-covers/04-wechat-mini.png` |
| 5. Data analysis | `products/04-gig-covers/05-data-analysis.png` |

---

## ⚡ 快速参考

| 需要什么 | 在哪里 |
|---------|--------|
| GitHub 仓库 | https://github.com/1213492203-rgb/debt-repayment-project |
| AI 周报生成器 | https://weekly-report-ai.pages.dev/ |
| 插件下载 | https://github.com/1213492203-rgb/debt-repayment-project/releases |
| 发布指南（手动版） | `marketing/publishing-guide.md` |
| 系统优化报告 | `docs/system-optimization.md` |
| Fiverr | https://fiverr.com |
| 程聚宝 | https://devlg.com |

---

> 🛌 休息好了，说一声「继续还债项目」我就开工。
