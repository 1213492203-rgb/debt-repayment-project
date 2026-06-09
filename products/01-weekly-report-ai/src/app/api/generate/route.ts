import { NextRequest, NextResponse } from "next/server";

const TEMPLATE_PROMPTS: Record<string, string> = {
  professional: `你是一位资深职场汇报专家。请根据以下信息生成一份**专业正式**风格的周报。
要求：
- 使用正式但不过于死板的语言
- 结构清晰，分「本周工作概述」「重点工作详述」「成果与亮点」「存在的问题与风险」「下周工作计划」五个板块
- 适当包装工作成果，但不夸大
- 长度在500-800字`,

  casual: `你是一位友善的团队伙伴。请根据以下信息生成一份**轻松口语化**风格的周报，适合发在团队群里。
要求：
- 语气轻松自然，像在跟同事聊天
- 适当使用emoji增加亲和力
- 结构简单：做了啥 → 有什么收获 → 遇到啥坑 → 下周准备搞啥
- 长度在300-500字`,

  "data-driven": `你是一位数据分析师。请根据以下信息生成一份**数据驱动**风格的周报。
要求：
- 尽可能用量化指标描述工作（如完成度%、提升比例、处理数量等）
- 用户未提供具体数据时，根据描述合理推断并标注为「预估」
- 使用「关键指标」「数据洞察」「趋势分析」等板块
- 长度在400-600字`,

  brief: `你是一位追求效率的管理顾问。请根据以下信息生成一份**极简要点式**周报。
要求：
- 纯列点形式，每点不超过2行
- 按「完成」「进行中」「计划」「风险」四个维度分类
- 每条前加状态标签（✅完成 / 🔄进行中 / 📋计划 / ⚠️风险）
- 总计控制在15条以内`,
};

export async function POST(request: NextRequest) {
  try {
    const { workItems, achievements, challenges, nextWeekPlan, template } =
      await request.json();

    if (!workItems?.trim()) {
      return NextResponse.json(
        { error: "请填写本周工作内容" },
        { status: 400 }
      );
    }

    const templatePrompt =
      TEMPLATE_PROMPTS[template as string] || TEMPLATE_PROMPTS.professional;

    const systemPrompt = `${templatePrompt}

请严格按照以下JSON格式返回，不要包含其他内容：
{"report": "生成的周报内容（使用Markdown格式，\\n换行）"}`;

    const userMessage = `请根据以下信息生成周报：

【本周工作内容】
${workItems}

【本周成果/亮点】
${achievements || "（未填写）"}

【遇到的困难/风险】
${challenges || "（未填写）"}

【下周计划】
${nextWeekPlan || "（未填写）"}`;

    // Try Anthropic API first, fall back to a built-in template
    const apiKey = process.env.ANTHROPIC_API_KEY;

    if (apiKey) {
      try {
        const response = await fetch("https://api.anthropic.com/v1/messages", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-api-key": apiKey,
            "anthropic-version": "2023-06-01",
          },
          body: JSON.stringify({
            model: "claude-sonnet-4-6",
            max_tokens: 2048,
            system: systemPrompt,
            messages: [{ role: "user", content: userMessage }],
          }),
        });

        if (response.ok) {
          const data = await response.json();
          const content = data.content[0]?.text || "";
          // Parse JSON response from Claude
          try {
            const parsed = JSON.parse(content);
            return NextResponse.json({ report: parsed.report });
          } catch {
            // If Claude didn't return valid JSON, use the raw text
            return NextResponse.json({ report: content });
          }
        }
        console.error("Anthropic API error:", response.status, await response.text());
      } catch (apiErr) {
        console.error("Anthropic API call failed:", apiErr);
      }
    }

    // Fallback: Generate a well-structured report without external API
    const report = generateFallbackReport(
      workItems,
      achievements,
      challenges,
      nextWeekPlan,
      template as string
    );

    return NextResponse.json({ report });
  } catch (err) {
    console.error("Generate API error:", err);
    return NextResponse.json(
      { error: "生成失败，请稍后重试" },
      { status: 500 }
    );
  }
}

function generateFallbackReport(
  workItems: string,
  achievements: string,
  challenges: string,
  nextWeekPlan: string,
  template: string
): string {
  const now = new Date();
  const monday = new Date(now);
  monday.setDate(now.getDate() - ((now.getDay() + 6) % 7));
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);

  const dateStr = `${monday.getMonth() + 1}月${monday.getDate()}日 - ${sunday.getMonth() + 1}月${sunday.getDate()}日`;

  const workLines = workItems
    .split(/[；;。\n]/)
    .filter(Boolean)
    .map((s) => s.trim());
  const achieveLines = achievements
    .split(/[；;。\n]/)
    .filter(Boolean)
    .map((s) => s.trim());
  const challengeLines = challenges
    .split(/[；;。\n]/)
    .filter(Boolean)
    .map((s) => s.trim());
  const planLines = nextWeekPlan
    .split(/[；;。\n]/)
    .filter(Boolean)
    .map((s) => s.trim());

  if (template === "brief") {
    let report = `📋 **本周工作总结** (${dateStr})\n\n`;
    report += `**✅ 已完成**\n`;
    workLines.forEach((w) => (report += `- ${w}\n`));
    if (achieveLines.length > 0) {
      report += `\n**🏆 成果亮点**\n`;
      achieveLines.forEach((a) => (report += `- ${a}\n`));
    }
    if (challengeLines.length > 0) {
      report += `\n**⚠️ 风险/问题**\n`;
      challengeLines.forEach((c) => (report += `- ${c}\n`));
    }
    if (planLines.length > 0) {
      report += `\n**📋 下周计划**\n`;
      planLines.forEach((p) => (report += `- ${p}\n`));
    }
    return report;
  }

  if (template === "data-driven") {
    let report = `## 📊 本周工作数据报告\n`;
    report += `**统计周期：**${dateStr}\n\n`;
    report += `### 📈 关键指标\n`;
    report += `- 本周任务总量：**${workLines.length} 项**\n`;
    report += `- 已完成率：约 **${Math.min(95, 80 + Math.floor(Math.random() * 15))}%**（预估）\n`;

    if (achieveLines.length > 0) {
      report += `- 亮点成果：**${achieveLines.length} 项**\n`;
    }
    report += `\n### 📋 工作明细\n`;
    workLines.forEach((w, i) => (report += `${i + 1}. ${w} ✅\n`));

    if (achieveLines.length > 0) {
      report += `\n### 🏆 数据洞察\n`;
      achieveLines.forEach((a) => (report += `- ${a}\n`));
    }
    if (challengeLines.length > 0) {
      report += `\n### ⚠️ 风险预警\n`;
      challengeLines.forEach((c) => (report += `- ${c}\n`));
    }
    if (planLines.length > 0) {
      report += `\n### 🎯 下周规划\n`;
      planLines.forEach((p) => (report += `- ${p}\n`));
    }
    return report;
  }

  if (template === "casual") {
    let report = `嘿嘿，又到了一周一次的周报时间啦！📝\n\n`;
    report += `**🗓️ ${dateStr}**\n\n`;
    report += `这周主要搞了这些事：\n`;
    workLines.forEach((w) => (report += `- ${w}\n`));

    if (achieveLines.length > 0) {
      report += `\n💪 **这周的收获：**\n`;
      achieveLines.forEach((a) => (report += `- ${a}\n`));
    }
    if (challengeLines.length > 0) {
      report += `\n😤 **踩过的坑：**\n`;
      challengeLines.forEach((c) => (report += `- ${c}\n`));
    }
    if (planLines.length > 0) {
      report += `\n🚀 **下周准备冲：**\n`;
      planLines.forEach((p) => (report += `- ${p}\n`));
    }
    report += `\n总结就是：干了不少活，下周继续卷！💪`;
    return report;
  }

  // Professional (default)
  let report = `## 本周工作周报\n\n`;
  report += `**汇报周期：**${dateStr}\n`;
  report += `**汇报人：** [您的姓名]\n\n`;
  report += `---\n\n`;

  report += `### 一、本周工作概述\n\n`;
  report += `本周共完成 **${workLines.length}** 项重点工作，总体进展顺利`;
  if (achieveLines.length > 0) {
    report += `，取得 **${achieveLines.length}** 项阶段性成果`;
  }
  report += `。\n\n`;

  report += `### 二、重点工作详述\n\n`;
  workLines.forEach((w, i) => {
    report += `**${i + 1}. ${w}**\n`;
    report += `- 状态：✅ 已完成\n`;
    report += `- 产出：按计划推进，达到预期目标\n\n`;
  });

  if (achieveLines.length > 0) {
    report += `### 三、成果与亮点\n\n`;
    achieveLines.forEach((a) => (report += `- 🏆 ${a}\n`));
    report += `\n`;
  }

  if (challengeLines.length > 0) {
    report += `### 四、存在的问题与风险\n\n`;
    challengeLines.forEach((c) => (report += `- ⚠️ ${c}\n`));
    report += "\n**应对措施：** 已制定应对方案，将持续跟踪推进。\n\n";
  }

  if (planLines.length > 0) {
    report += `### 五、下周工作计划\n\n`;
    planLines.forEach((p, i) => (report += `${i + 1}. 📋 ${p}\n`));
  }

  report += `\n---\n`;
  report += `*本报告由 AI周报生成器 自动生成*`;
  return report;
}
