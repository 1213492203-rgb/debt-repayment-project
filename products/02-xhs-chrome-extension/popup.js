// ===== popup.js - Main Extension Logic =====

const API_ENDPOINT = "https://api.anthropic.com/v1/messages";
const MAX_FREE_USES = 5;

// Tab switching
document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document
      .querySelectorAll(".tab")
      .forEach((t) => t.classList.remove("active"));
    document
      .querySelectorAll(".tab-content")
      .forEach((c) => c.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(`tab-${tab.dataset.tab}`).classList.add("active");
  });
});

// Usage tracking
async function getUsageCount() {
  const today = new Date().toISOString().split("T")[0];
  const { [today]: count } = await chrome.storage.local.get(today);
  return count || 0;
}

async function incrementUsage() {
  const today = new Date().toISOString().split("T")[0];
  const count = await getUsageCount();
  await chrome.storage.local.set({ [today]: count + 1 });
  updateUsageDisplay();
}

async function updateUsageDisplay() {
  const count = await getUsageCount();
  const remaining = Math.max(0, MAX_FREE_USES - count);
  document.getElementById("usage-count").textContent = remaining;
  if (remaining === 0) {
    document.getElementById("usage-count").style.color = "#ff2442";
  }
}

// API Key management
async function getApiKey() {
  const { apiKey } = await chrome.storage.local.get("apiKey");
  return apiKey || "";
}

async function callAI(systemPrompt: string, userMessage: string): Promise<string> {
  const apiKey = await getApiKey();

  if (!apiKey) {
    // Fallback: use built-in templates
    return generateWithTemplates(systemPrompt, userMessage);
  }

  try {
    const res = await fetch(API_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-6",
        max_tokens: 1024,
        system: systemPrompt,
        messages: [{ role: "user", content: userMessage }],
      }),
    });

    if (res.ok) {
      const data = await res.json();
      return data.content[0]?.text || "";
    }
  } catch (e) {
    console.error("API call failed:", e);
  }

  return generateWithTemplates(systemPrompt, userMessage);
}

// Built-in templates (fallback when no API key)
function generateWithTemplates(systemPrompt: string, userMessage: string): string {
  // Title templates
  if (systemPrompt.includes("标题")) {
    const keywords = extractKeywords(userMessage);
    return generateTitleTemplates(keywords);
  }
  // Content templates
  if (systemPrompt.includes("正文")) {
    const topic = extractTopic(userMessage);
    const points = extractPoints(userMessage);
    return generateContentTemplate(topic, points);
  }
  // Hashtag templates
  if (systemPrompt.includes("标签")) {
    const topic = extractTopic(userMessage);
    return generateHashtagTemplate(topic);
  }
  return "请配置 API Key 以获得更好的生成效果";
}

function extractKeywords(msg: string): string {
  const match = msg.match(/关键词[：:]\s*(.+)/);
  return match ? match[1] : msg.substring(0, 50);
}

function extractTopic(msg: string): string {
  const match = msg.match(/主题[：:]\s*(.+)/);
  return match ? match[1] : msg.substring(0, 50);
}

function extractPoints(msg: string): string[] {
  const match = msg.match(/核心要点[：:]\s*([\s\S]+?)(?:语气|$)/);
  if (match) {
    return match[1]
      .split(/\n/)
      .filter((s) => s.trim())
      .map((s) => s.replace(/^[-\d.]+\s*/, "").trim());
  }
  return [];
}

function generateTitleTemplates(keywords: string): string {
  const templates = [
    `🔥 绝了！关于${keywords}，我发现了这些宝藏秘密`,
    `别再乱踩坑了！${keywords}的超全攻略来了 📝`,
    `0基础也能轻松上手！${keywords}保姆级教程 ✨`,
    `闺蜜问我100遍的${keywords}秘诀，今天我公开了`,
    `从入门到精通，${keywords}看这篇就够了 💯`,
    `没人敢说的${keywords}真相，今天我来说...`,
    `后悔没早知道！${keywords}的5个神仙技巧`,
    `3天实测！${keywords}到底值不值得冲？`,
  ];

  return (
    "🎯 为你生成的高转化标题：\n\n" +
    templates
      .slice(0, 5)
      .map((t, i) => `${i + 1}. ${t}`)
      .join("\n")
  );
}

function generateContentTemplate(
  topic: string,
  points: string[]
): string {
  let content = `📝 **${topic || "笔记正文"}**\n\n`;
  content += `哈喽姐妹们！今天来分享一下关于${topic || "这个话题"}的心得～\n\n`;

  if (points.length > 0) {
    points.forEach((p, i) => {
      content += `${i + 1}️⃣ ${p}\n`;
      content += `这一点真的太重要了，我亲测有效！\n\n`;
    });
  } else {
    content += `作为一个深度体验者，我真的有话要说...\n\n`;
    content += `✨ 亮点一：[请在此填写]\n`;
    content += `✨ 亮点二：[请在此填写]\n`;
    content += `✨ 亮点三：[请在此填写]\n\n`;
  }

  content += `💡 **总结**：总之，${
    topic || "这次体验"
  }真的超出预期，强烈推荐给各位姐妹！\n\n`;
  content += `如果觉得有用记得点赞收藏哦～💕`;

  return content;
}

function generateHashtagTemplate(topic: string): string {
  const generalTags = [
    "日常分享",
    "好物推荐",
    "真实测评",
    "干货分享",
    "新人求关注",
  ];
  const categoryTags: Record<string, string[]> = {
    beauty: ["美妆", "护肤", "化妆品", "素颜", "变美"],
    fashion: ["穿搭", "OOTD", "时尚", "日常穿搭", "显瘦"],
    food: ["美食", "探店", "吃货", "周末去哪", "下午茶"],
    travel: ["旅行", "攻略", "打卡", "小众景点", "周末游"],
    lifestyle: ["生活", "家居", "好物", "仪式感", "治愈"],
    tech: ["数码", "科技", "手机", "电子产品", "效率工具"],
    fitness: ["健身", "减肥", "运动", "自律", "马甲线"],
    study: ["学习", "成长", "读书", "职场", "自我提升"],
  };

  const cat = document.getElementById("hashtag-type") as HTMLSelectElement;
  const catValue = cat?.value || "lifestyle";
  const specificTags = categoryTags[catValue] || generalTags;

  const allTags = [...specificTags, ...generalTags, topic].filter(Boolean);

  return (
    "🏷️ **推荐标签：**\n\n" +
    allTags.map((t) => `#${t}`).join("  ") +
    "\n\n" +
    `💡 提示：建议使用 5-10 个标签，前3个最重要！`
  );
}

// ===== Event Handlers =====

// Title Generation
document.getElementById("generate-title")?.addEventListener("click", async () => {
  const keywords = (document.getElementById("title-keywords") as HTMLInputElement)
    .value;
  const style = (document.getElementById("title-style") as HTMLSelectElement).value;
  const audience = (
    document.getElementById("title-audience") as HTMLInputElement
  ).value;

  if (!keywords.trim()) {
    alert("请输入笔记主题或关键词");
    return;
  }

  const count = await getUsageCount();
  if (count >= MAX_FREE_USES) {
    alert("今日免费次数已用完，请升级高级版继续使用");
    return;
  }

  const btn = document.getElementById("generate-title") as HTMLButtonElement;
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> 生成中...';

  const result = await callAI(
    `你是一个小红书爆款标题专家。请根据用户提供的关键词、风格和受众，生成5个高点击率的标题。
规则：
- 标题不超过20字
- 使用emoji增强吸引力
- 风格：${style === "catchy" ? "吸睛、使用感叹号和夸张表达" : ""}${style === "emotional" ? "情感共鸣、走心温暖" : ""}${style === "list" ? "使用数字、清单体" : ""}${style === "question" ? "反问句式、引发好奇" : ""}${style === "contrast" ? "对比反差、制造悬念" : ""}
- 目标受众：${audience || "年轻女性"}
- 每个标题一行，格式：1. 标题`,
    `请为以下主题生成标题：${keywords}`
  );

  const resultDiv = document.getElementById("title-result")!;
  resultDiv.classList.remove("hidden");
  resultDiv.innerHTML = `${result}<button class="copy-btn" onclick="navigator.clipboard.writeText(this.previousSibling.textContent.trim())">📋 一键复制</button>`;

  btn.disabled = false;
  btn.innerHTML = '<span class="btn-icon">✨</span> 生成5个标题';
  await incrementUsage();
});

// Content Generation
document.getElementById("generate-content")?.addEventListener("click", async () => {
  const topic = (document.getElementById("content-topic") as HTMLInputElement)
    .value;
  const points = (document.getElementById("content-points") as HTMLTextAreaElement)
    .value;
  const tone = (document.getElementById("content-tone") as HTMLSelectElement).value;

  if (!topic.trim()) {
    alert("请输入主题");
    return;
  }

  const count = await getUsageCount();
  if (count >= MAX_FREE_USES) {
    alert("今日免费次数已用完");
    return;
  }

  const btn = document.getElementById("generate-content") as HTMLButtonElement;
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> 撰写中...';

  const result = await callAI(
    `你是一个小红书文案专家。请撰写一篇小红书笔记正文。
要求：
- 语气风格：${tone}
- 使用emoji和分段增强可读性
- 开头吸引人，结尾有互动引导（点赞收藏）
- 300-500字`,
    `主题：${topic}\n核心要点：${points}`
  );

  const resultDiv = document.getElementById("content-result")!;
  resultDiv.classList.remove("hidden");
  resultDiv.innerHTML = `${result}<button class="copy-btn" onclick="navigator.clipboard.writeText(this.previousSibling.textContent.trim())">📋 一键复制</button>`;

  btn.disabled = false;
  btn.innerHTML = '<span class="btn-icon">📝</span> 生成正文';
  await incrementUsage();
});

// Hashtag Generation
document.getElementById("generate-hashtag")?.addEventListener("click", async () => {
  const topic = (document.getElementById("hashtag-topic") as HTMLInputElement)
    .value;
  const type = (document.getElementById("hashtag-type") as HTMLSelectElement)
    .value;

  if (!topic.trim()) {
    alert("请输入笔记主题");
    return;
  }

  const count = await getUsageCount();
  if (count >= MAX_FREE_USES) {
    alert("今日免费次数已用完");
    return;
  }

  const btn = document.getElementById("generate-hashtag") as HTMLButtonElement;
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> 推荐中...';

  const result = await callAI(
    `你是一个小红书运营专家。请为用户的笔记推荐10-15个热门标签。
要求：
- 包含大流量标签（百万级）和精准长尾标签
- 按流量从大到小排列
- 每个标签格式：#标签名
- 笔记类型：${type}`,
    `笔记主题：${topic}`
  );

  const resultDiv = document.getElementById("hashtag-result")!;
  resultDiv.classList.remove("hidden");
  resultDiv.innerHTML = `${result}<button class="copy-btn" onclick="navigator.clipboard.writeText(this.previousSibling.textContent.trim())">📋 一键复制</button>`;

  btn.disabled = false;
  btn.innerHTML = '<span class="btn-icon">#</span> 推荐标签';
  await incrementUsage();
});

// Upgrade button
document.getElementById("upgrade-btn")?.addEventListener("click", () => {
  chrome.tabs.create({
    url: "https://your-payment-page.com/upgrade", // TODO: Replace with actual payment link
  });
});

// Feedback link
document.getElementById("feedback-link")?.addEventListener("click", (e) => {
  e.preventDefault();
  chrome.tabs.create({
    url: "mailto:xiaohongshu.helper@proton.me",
  });
});

// Initialize
updateUsageDisplay();
