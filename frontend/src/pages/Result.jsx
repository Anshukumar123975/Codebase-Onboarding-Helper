import MarkdownResult from "../components/MarkdownResult";
import CodebaseChat from "../components/CodebaseChat";

export default function Result({ markdown, jobId, onReset }) {
  return (
    <div className="py-10 px-4">
      <div className="w-full max-w-7xl mx-auto grid gap-6 lg:grid-cols-[minmax(0,1fr)_380px] items-start">
        <MarkdownResult markdown={markdown} onReset={onReset} />
        <CodebaseChat jobId={jobId} />
      </div>
    </div>
  );
}
