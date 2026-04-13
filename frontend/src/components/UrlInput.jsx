import { useState } from "react";

const EXAMPLES = [
  "https://github.com/expressjs/express",
  "https://github.com/pallets/flask",
  "https://github.com/tiangolo/fastapi",
];

export default function UrlInput({ onSubmit, loading }) {
  const [url, setUrl] = useState("");
  const [error, setError] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    setError("");
    const trimmed = url.trim();
    if (!trimmed.startsWith("https://github.com/")) {
      setError("Please enter a valid public GitHub repository URL");
      return;
    }
    onSubmit(trimmed);
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      <form onSubmit={handleSubmit} className="flex gap-3">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://github.com/user/repo"
          disabled={loading}
          className="flex-1 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={loading || !url.trim()}
          className="px-6 py-3 bg-emerald-600 hover:bg-emerald-500 disabled:bg-gray-700 disabled:text-gray-500 text-white font-medium rounded-lg transition-colors"
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {error && (
        <p className="mt-2 text-red-400 text-sm">{error}</p>
      )}

      <div className="mt-6 text-sm text-gray-500">
        <p className="mb-2">Try an example:</p>
        <div className="flex flex-wrap gap-2">
          {EXAMPLES.map((ex) => (
            <button
              key={ex}
              onClick={() => setUrl(ex)}
              disabled={loading}
              className="px-3 py-1 bg-gray-800 border border-gray-700 rounded-md hover:border-gray-500 transition-colors text-gray-400 hover:text-gray-200 disabled:opacity-50"
            >
              {ex.replace("https://github.com/", "")}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
