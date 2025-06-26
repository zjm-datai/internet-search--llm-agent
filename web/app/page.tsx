// app/page.tsx
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main className="flex flex-col min-h-screen bg-white">

      <nav className="h-20 flex items-center border-b border-gray-200 w-full max-w-screen-xl mx-auto px-8 md:px-16">
        <h1 className="text-2xl font-bold text-blue-600">智搜</h1>
        <div className="flex-1" />
        <div className="hidden md:flex space-x-8 text-gray-600">
          <Link href="#">产品</Link>
          <Link href="#">文档</Link>
          <Link href="#">案例</Link>
          <Link href="#">博客</Link>
        </div>
        <div className="flex items-center space-x-4">
          <a
            href="https://github.com/your-repo"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center text-gray-600 hover:text-gray-900"
          >
            <svg className="w-5 h-5 ml-4" fill="currentColor" viewBox="0 0 24 24">
              <path
                fillRule="evenodd"
                d="M12 2C6.477 2 2 6.484 2 12.017c0 4.426 2.865 8.183 6.839 9.504.5.092.682-.217.682-.482
                   0-.237-.009-.866-.014-1.699-2.782.605-3.369-1.343-3.369-1.343-.454-1.155-1.11-1.463-1.11-1.463
                   -.908-.62.069-.607.069-.607 1.003.07 1.531 1.031 1.531 1.031.892 1.529 2.341 1.087 2.91.832
                   .092-.647.35-1.087.636-1.337-2.22-.253-4.555-1.113-4.555-4.951
                   0-1.093.39-1.988 1.03-2.688-.103-.253-.447-1.272.098-2.65
                   0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844a9.56 9.56 0 012.5.336
                   c1.91-1.296 2.75-1.026 2.75-1.026.546 1.378.202 2.397.1 2.65
                   .64.7 1.03 1.595 1.03 2.688 0 3.848-2.338 4.695-4.566 4.943
                   .36.31.68.92.68 1.852 0 1.337-.012 2.419-.012 2.747
                   0 .268.18.58.688.482A10.02 10.02 0 0022 12.017C22 6.484 17.523 2 12 2z"
                clipRule="evenodd"
              />
            </svg>
            104.7k
          </a>
          <Button asChild>
            <Link href="/chat">开始体验</Link>
          </Button>
        </div>
      </nav>

      <section className="flex-grow w-full max-w-screen-xl mx-auto grid grid-cols-12 items-center gap-0 px-8 md:px-16 pb-24">
        <div className="col-span-12 md:col-span-6 flex flex-col space-y-8 pr-8">
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-extrabold leading-tight text-gray-900 whitespace-nowrap">
            <span>优雅的</span>{" "}
            <span className="text-blue-600">智能搜索</span>{" "}
            <span>与推理平台</span> 
          </h1>
          {/* <div className="text-lg text-gray-600">• GitHub 上的 104.7k 颗星</div> */}
          <p className="text-xl md:text-2xl text-gray-600 max-w-md whitespace-nowrap">
            实时互联网检索 + 大模型推理，构建自主知识图谱，洞察更深、答案更准。
          </p>
        </div>
      </section>
    </main>
  );
}

