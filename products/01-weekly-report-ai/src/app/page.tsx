"use client";

import { useState, useRef } from "react";

type Template = "professional" | "casual" | "data-driven" | "brief";

interface ReportData {
  workItems: string;
  achievements: string;
  challenges: string;
  nextWeekPlan: string;
  template: Template;
}

export default function Home() {
  const [formData, setFormData] = useState<ReportData>({
    workItems: "",
    achievements: "",
    challenges: "",
    nextWeekPlan: "",
    template: "professional",
  });
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const reportRef = useRef<HTMLDivElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!formData.workItems.trim()) {
      setError("请至少填写「本周工作内容」");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || "生成失败");
      }
      setReport(data.report);
    } catch (err) {
      setError(err instanceof Error ? err.message : "生成失败，请重试");
    } finally {
      setLoading(false);
    }
  };

  const copyReport = async () => {
    if (report) {
      await navigator.clipboard.writeText(report);
      alert("已复制到剪贴板！");
    }
  };

  const templates: { key: Template; label: string; desc: string }[] = [
    { key: "professional", label: "专业正式", desc: "适合向领导汇报" },
    { key: "casual", label: "轻松口语化", desc: "适合团队内部同步" },
    { key: "data-driven", label: "数据驱动", desc: "突出量化成果" },
    { key: "brief", label: "简洁要点", desc: "列点式快速浏览" },
  ];

  return (
    <div className="min-h-screen">
      {/* Header / Hero */}
      <header className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
        <div className="max-w-4xl mx-auto px-4 py-16 sm:py-24 text-center">
          <p className="text-indigo-200 text-sm font-medium mb-3">
            🔥 国内首个 AI 周报生成工具
          </p>
          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight mb-4">
            1 分钟搞定让人头疼的周报
          </h1>
          <p className="text-lg sm:text-xl text-indigo-100 max-w-2xl mx-auto mb-8">
            输入你的工作关键词，AI 秒级生成结构清晰、重点突出的专业周报。
            每周五下午不再煎熬！
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm">
            <span className="bg-white/20 px-4 py-2 rounded-full">
              📝 支持多风格模板
            </span>
            <span className="bg-white/20 px-4 py-2 rounded-full">
              ⚡ 10 秒生成
            </span>
            <span className="bg-white/20 px-4 py-2 rounded-full">
              📋 一键复制
            </span>
            <span className="bg-white/20 px-4 py-2 rounded-full">
              🔒 数据不存储
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-12">
        <div className="grid lg:grid-cols-5 gap-8">
          {/* Input Form */}
          <div className="lg:col-span-2">
            <form
              onSubmit={handleSubmit}
              className="bg-white rounded-2xl shadow-lg p-6 space-y-5 sticky top-6"
            >
              <h2 className="text-xl font-bold text-gray-800">
                📝 填写工作内容
              </h2>

              {/* Template Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-2">
                  选择风格
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {templates.map((t) => (
                    <button
                      key={t.key}
                      type="button"
                      onClick={() =>
                        setFormData({ ...formData, template: t.key })
                      }
                      className={`text-left px-3 py-2 rounded-lg text-sm border transition-all ${
                        formData.template === t.key
                          ? "border-indigo-500 bg-indigo-50 text-indigo-700 shadow-sm"
                          : "border-gray-200 hover:border-gray-300 text-gray-600"
                      }`}
                    >
                      <div className="font-medium">{t.label}</div>
                      <div className="text-xs opacity-70">{t.desc}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Work Items */}
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1">
                  本周工作内容 <span className="text-red-500">*</span>
                </label>
                <textarea
                  rows={4}
                  placeholder="例：完成用户登录模块开发；修复3个线上bug；参加2次需求评审会..."
                  value={formData.workItems}
                  onChange={(e) =>
                    setFormData({ ...formData, workItems: e.target.value })
                  }
                  className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition resize-none"
                />
              </div>

              {/* Achievements */}
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1">
                  本周成果/亮点
                </label>
                <textarea
                  rows={3}
                  placeholder="例：新功能上线后转化率提升15%；完成了积压的10个技术需求..."
                  value={formData.achievements}
                  onChange={(e) =>
                    setFormData({ ...formData, achievements: e.target.value })
                  }
                  className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition resize-none"
                />
              </div>

              {/* Challenges */}
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1">
                  遇到的困难/风险
                </label>
                <textarea
                  rows={2}
                  placeholder="例：第三方API响应慢，已与对方沟通优化方案..."
                  value={formData.challenges}
                  onChange={(e) =>
                    setFormData({ ...formData, challenges: e.target.value })
                  }
                  className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition resize-none"
                />
              </div>

              {/* Next Week Plan */}
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1">
                  下周计划
                </label>
                <textarea
                  rows={3}
                  placeholder="例：启动支付模块开发；优化首页加载性能..."
                  value={formData.nextWeekPlan}
                  onChange={(e) =>
                    setFormData({ ...formData, nextWeekPlan: e.target.value })
                  }
                  className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition resize-none"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold py-3.5 px-6 rounded-xl hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all btn-glow text-lg"
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                        fill="none"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                      />
                    </svg>
                    AI 正在生成中...
                  </span>
                ) : (
                  "✨ 一键生成周报"
                )}
              </button>

              {error && (
                <p className="text-red-500 text-sm bg-red-50 px-4 py-2 rounded-lg">
                  {error}
                </p>
              )}
            </form>
          </div>

          {/* Output Area */}
          <div className="lg:col-span-3" ref={reportRef}>
            {!report && !loading && (
              <div className="bg-white rounded-2xl shadow-lg p-12 text-center">
                <div className="text-6xl mb-4">📄</div>
                <h3 className="text-xl font-semibold text-gray-700 mb-2">
                  你的周报将在这里显示
                </h3>
                <p className="text-gray-400">
                  填写左侧表单后点击「生成周报」，AI 将为你自动撰写
                </p>
              </div>
            )}

            {loading && (
              <div className="bg-white rounded-2xl shadow-lg p-12 text-center">
                <div className="animate-pulse space-y-4">
                  <div className="h-4 bg-gray-200 rounded w-3/4 mx-auto"></div>
                  <div className="h-4 bg-gray-200 rounded w-1/2 mx-auto"></div>
                  <div className="h-4 bg-gray-200 rounded w-5/6 mx-auto"></div>
                  <div className="h-4 bg-gray-200 rounded w-2/3 mx-auto"></div>
                  <div className="h-4 bg-gray-200 rounded w-3/4 mx-auto"></div>
                </div>
                <p className="text-gray-400 mt-6 text-sm">
                  AI 正在为你撰写周报，请稍候...
                </p>
              </div>
            )}

            {report && !loading && (
              <div className="bg-white rounded-2xl shadow-lg overflow-hidden animate-fade-in-up">
                <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-4 flex items-center justify-between">
                  <h3 className="text-white font-semibold text-lg">
                    ✅ 周报已生成
                  </h3>
                  <div className="flex gap-2">
                    <button
                      onClick={copyReport}
                      className="bg-white/20 hover:bg-white/30 text-white px-4 py-1.5 rounded-lg text-sm transition"
                    >
                      📋 复制
                    </button>
                    <button
                      onClick={() => setReport("")}
                      className="bg-white/20 hover:bg-white/30 text-white px-4 py-1.5 rounded-lg text-sm transition"
                    >
                      ✏️ 重新生成
                    </button>
                  </div>
                </div>
                <div className="p-6 sm:p-8">
                  <div className="prose prose-sm max-w-none whitespace-pre-wrap text-gray-800 leading-relaxed">
                    {report}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Features Section */}
        <section className="mt-20 mb-12">
          <h2 className="text-2xl font-bold text-center text-gray-800 mb-10">
            为什么选择 AI 周报生成器？
          </h2>
          <div className="grid sm:grid-cols-3 gap-6">
            {[
              {
                emoji: "⚡",
                title: "极速生成",
                desc: "输入关键词，10秒生成完整周报，告别两小时的冥思苦想",
              },
              {
                emoji: "🎨",
                title: "多风格模板",
                desc: "专业正式、轻松口语、数据驱动、简洁要点，总有一款适合你",
              },
              {
                emoji: "🧠",
                title: "AI智能润色",
                desc: "自动优化表达，让你的工作显得更有条理、更有价值",
              },
              {
                emoji: "🔒",
                title: "数据安全",
                desc: "我们不存储你的任何工作数据，生成后即销毁",
              },
              {
                emoji: "📱",
                title: "全平台使用",
                desc: "电脑、平板、手机均可使用，随时随地写周报",
              },
              {
                emoji: "💰",
                title: "完全免费",
                desc: "基础功能永久免费，高级功能即将上线",
              },
            ].map((f, i) => (
              <div
                key={i}
                className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition"
              >
                <div className="text-3xl mb-3">{f.emoji}</div>
                <h3 className="font-semibold text-gray-800 mb-1">{f.title}</h3>
                <p className="text-sm text-gray-500">{f.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Pricing Preview */}
        <section className="mb-12 text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            升级高级版，解锁更多能力
          </h2>
          <p className="text-gray-500 mb-8">
            基础版永久免费，高级版提供更强大的 AI 能力
          </p>
          <div className="grid sm:grid-cols-2 gap-6 max-w-2xl mx-auto">
            <div className="bg-white rounded-2xl shadow-sm p-8 border border-gray-200">
              <p className="text-sm font-medium text-gray-500 mb-2">基础版</p>
              <p className="text-4xl font-bold text-gray-800 mb-4">
                免费
              </p>
              <ul className="text-sm text-gray-500 space-y-2 mb-6 text-left">
                <li>✅ 每天 5 次生成</li>
                <li>✅ 4 种风格模板</li>
                <li>✅ 基础 AI 润色</li>
                <li>✅ 一键复制导出</li>
              </ul>
              <button className="w-full py-3 rounded-xl border-2 border-gray-200 text-gray-600 font-semibold hover:bg-gray-50 transition">
                开始使用
              </button>
            </div>
            <div className="bg-gradient-to-b from-indigo-600 to-purple-600 rounded-2xl shadow-lg p-8 text-white relative overflow-hidden">
              <div className="absolute top-0 right-0 bg-yellow-400 text-yellow-900 text-xs font-bold px-3 py-1 rounded-bl-lg">
                推荐
              </div>
              <p className="text-sm font-medium text-indigo-200 mb-2">高级版</p>
              <p className="text-4xl font-bold mb-1">
                ¥19<span className="text-lg font-normal">/月</span>
              </p>
              <p className="text-indigo-200 text-sm mb-4">即将上线</p>
              <ul className="text-sm space-y-2 mb-6 text-left">
                <li>✅ 无限次生成</li>
                <li>✅ 10+ 风格模板</li>
                <li>✅ 超强 AI 润色引擎</li>
                <li>✅ 历史记录保存</li>
                <li>✅ 自定义模板</li>
                <li>✅ 多项目管理</li>
              </ul>
              <div className="bg-white/20 rounded-xl px-4 py-2 text-sm">
                🔔 留下邮箱，上线第一时间通知
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white py-8 text-center text-sm text-gray-400">
        <p>© 2026 AI周报生成器 | 用AI让你的工作更高效</p>
        <p className="mt-1">
          联系我们：weeklyreport.ai@proton.me
        </p>
      </footer>
    </div>
  );
}
