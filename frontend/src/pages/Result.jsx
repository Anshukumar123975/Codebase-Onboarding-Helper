import MarkdownResult from "../components/MarkdownResult";

export default function Result({ markdown, onReset }) {
  return (
    <div className="py-10 px-4">
      <MarkdownResult markdown={markdown} onReset={onReset} />
    </div>
  );
}
