import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI周报生成器 - 智能写周报，1分钟搞定",
  description:
    "基于AI的智能周报生成工具，输入工作内容自动生成专业周报。支持多种风格模板，让你的周报脱颖而出。",
  keywords: ["周报生成", "AI周报", "工作汇报", "智能写作", "周报模板"],
  robots: "index, follow",
  openGraph: {
    title: "AI周报生成器 - 1分钟搞定专业周报",
    description: "输入工作关键词，AI自动生成专业周报。告别周五下午的煎熬！",
    type: "website",
    locale: "zh_CN",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className="antialiased min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
        {children}
      </body>
    </html>
  );
}
