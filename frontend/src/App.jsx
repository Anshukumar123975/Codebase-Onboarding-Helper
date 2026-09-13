import { useState, useEffect, useRef } from "react";
import Home from "./pages/Home";
import Processing from "./pages/Processing";
import Result from "./pages/Result";
import { startAnalysis, getStatus, getResult } from "./api/client";

const VIEW = { HOME: "home", PROCESSING: "processing", RESULT: "result" };

export default function App() {
  const [view, setView] = useState(VIEW.HOME);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [repoUrl, setRepoUrl] = useState("");
  const [jobId, setJobId] = useState(null);
  const [statusData, setStatusData] = useState({
    currentAgent: "",
    completedAgents: [],
    progressPercent: 0,
  });
  const [markdown, setMarkdown] = useState("");
  const pollRef = useRef(null);

  // Clean up polling on unmount
  useEffect(() => {
    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, []);

  async function handleSubmit(url) {
    setLoading(true);
    setError("");
    setRepoUrl(url);

    try {
      const { job_id } = await startAnalysis(url);
      setJobId(job_id);
      setView(VIEW.PROCESSING);
      startPolling(job_id);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function startPolling(id) {
    if (pollRef.current) clearInterval(pollRef.current);

    pollRef.current = setInterval(async () => {
      try {
        const data = await getStatus(id);
        setStatusData({
          currentAgent: data.current_agent,
          completedAgents: data.completed_agents,
          progressPercent: data.progress_percent,
        });

        if (data.status === "done") {
          clearInterval(pollRef.current);
          pollRef.current = null;
          const result = await getResult(id);
          setMarkdown(result.markdown);
          setView(VIEW.RESULT);
        }
      } catch (err) {
        clearInterval(pollRef.current);
        pollRef.current = null;
        setError(err.message);
        setView(VIEW.HOME);
      }
    }, 2000);
  }

  function handleReset() {
    setView(VIEW.HOME);
    setJobId(null);
    setMarkdown("");
    setStatusData({ currentAgent: "", completedAgents: [], progressPercent: 0 });
    setError("");
    setRepoUrl("");
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b border-gray-800 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <button onClick={handleReset} className="text-lg font-semibold text-white hover:text-emerald-400 transition-colors">
            Codebase Onboarder
          </button>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-500 hover:text-gray-300 text-sm"
          >
            GitHub
          </a>
        </div>
      </header>

      {/* Error banner */}
      {error && (
        <div className="max-w-2xl mx-auto mt-4 px-4">
          <div className="bg-red-900/30 border border-red-800 rounded-lg px-4 py-3 text-red-300 text-sm">
            {error}
            <button onClick={() => setError("")} className="ml-3 text-red-400 hover:text-red-200">&times;</button>
          </div>
        </div>
      )}

      {/* Main content */}
      {view === VIEW.HOME && (
        <Home onSubmit={handleSubmit} loading={loading} />
      )}
      {view === VIEW.PROCESSING && (
        <Processing
          repoUrl={repoUrl}
          currentAgent={statusData.currentAgent}
          completedAgents={statusData.completedAgents}
          progressPercent={statusData.progressPercent}
        />
      )}
      {view === VIEW.RESULT && (
        <Result markdown={markdown} jobId={jobId} onReset={handleReset} />
      )}
    </div>
  );
}
