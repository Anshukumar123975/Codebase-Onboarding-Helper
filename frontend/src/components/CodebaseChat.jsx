import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { sendChatMessage } from "../api/client";

const WELCOME = {
  role: "assistant",
  content: "Analysis complete. Ask me about the architecture, setup, data flow, or which files to read first.",
};

export default function CodebaseChat({ jobId }) {
  const [messages, setMessages] = useState([WELCOME]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const endRef = useRef(null);

  useEffect(() => {
    setMessages([WELCOME]);
    setInput("");
    setError("");
  }, [jobId]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSubmit(event) {
    event.preventDefault();
    const question = input.trim();
    if (!question || loading) return;

    const userMessage = { role: "user", content: question };
    const priorHistory = messages.slice(1).slice(-12);
    setMessages((current) => [...current, userMessage]);
    setInput("");
    setError("");
    setLoading(true);

    try {
      const { answer } = await sendChatMessage(jobId, question, priorHistory);
      setMessages((current) => [...current, { role: "assistant", content: answer }]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <aside className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden lg:sticky lg:top-6">
      <div className="border-b border-gray-800 px-5 py-4">
        <h2 className="text-white font-semibold">Ask about this codebase</h2>
        <p className="text-gray-500 text-xs mt-1">Answers are grounded in the generated analysis.</p>
      </div>

      <div className="h-[480px] overflow-y-auto px-4 py-4 space-y-4" aria-live="polite">
        {messages.map((message, index) => (
          <div key={`${message.role}-${index}`} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`chat-message max-w-[88%] rounded-xl px-3.5 py-2.5 text-sm ${message.role === "user" ? "bg-emerald-600 text-white" : "bg-gray-800 text-gray-200"}`}>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
            </div>
          </div>
        ))}
        {loading && <div className="text-gray-500 text-sm animate-pulse">Thinking...</div>}
        <div ref={endRef} />
      </div>

      <form onSubmit={handleSubmit} className="border-t border-gray-800 p-3">
        {error && <p className="text-red-400 text-xs mb-2">{error}</p>}
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                event.currentTarget.form?.requestSubmit();
              }
            }}
            placeholder="How does authentication work?"
            maxLength={2000}
            rows={2}
            className="flex-1 resize-none bg-gray-950 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-600 focus:outline-none focus:border-emerald-500"
          />
          <button type="submit" disabled={loading || !input.trim()} className="self-end px-3 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:bg-gray-700 disabled:text-gray-500 text-white text-sm font-medium rounded-lg transition-colors">
            Send
          </button>
        </div>
      </form>
    </aside>
  );
}
