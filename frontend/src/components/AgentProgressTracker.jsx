const AGENTS = [
  { key: "architecture", label: "Architecture Analysis" },
  { key: "setup", label: "Setup & Config" },
  { key: "code_flow", label: "Code Flow Analysis" },
  { key: "writer", label: "Writing Document" },
];

function CheckIcon() {
  return (
    <svg className="w-5 h-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
    </svg>
  );
}

function Spinner() {
  return (
    <div className="w-5 h-5 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin" />
  );
}

function Dot() {
  return <div className="w-3 h-3 bg-gray-600 rounded-full" />;
}

export default function AgentProgressTracker({ currentAgent, completedAgents, progressPercent }) {
  return (
    <div className="w-full max-w-lg mx-auto">
      {/* Progress bar */}
      <div className="mb-8">
        <div className="flex justify-between text-sm text-gray-400 mb-2">
          <span>Progress</span>
          <span>{progressPercent}%</span>
        </div>
        <div className="w-full h-2 bg-gray-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-emerald-500 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Agent steps */}
      <div className="space-y-4">
        {AGENTS.map((agent, i) => {
          const isDone = completedAgents.includes(agent.key);
          const isActive = currentAgent === agent.key;
          const isPending = !isDone && !isActive;

          return (
            <div key={agent.key} className="flex items-center gap-4">
              {/* Connector line */}
              <div className="flex flex-col items-center">
                <div className={`flex items-center justify-center w-8 h-8 rounded-full border-2 ${
                  isDone
                    ? "border-emerald-500 bg-emerald-500/10"
                    : isActive
                    ? "border-emerald-400 bg-emerald-400/10 animate-pulse-glow"
                    : "border-gray-700 bg-gray-800"
                }`}>
                  {isDone ? <CheckIcon /> : isActive ? <Spinner /> : <Dot />}
                </div>
                {i < AGENTS.length - 1 && (
                  <div className={`w-0.5 h-6 mt-1 ${isDone ? "bg-emerald-500/50" : "bg-gray-700"}`} />
                )}
              </div>

              {/* Label */}
              <span className={`text-sm font-medium ${
                isDone
                  ? "text-emerald-400"
                  : isActive
                  ? "text-white"
                  : "text-gray-500"
              }`}>
                {agent.label}
                {isActive && <span className="ml-2 text-gray-500">running...</span>}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
