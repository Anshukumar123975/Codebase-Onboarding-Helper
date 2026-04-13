import AgentProgressTracker from "../components/AgentProgressTracker";

export default function Processing({ currentAgent, completedAgents, progressPercent, repoUrl }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] px-4">
      <div className="mb-10 text-center">
        <h2 className="text-2xl font-bold text-white mb-2">Analyzing Repository</h2>
        <p className="text-gray-400 text-sm font-mono">{repoUrl}</p>
      </div>
      <AgentProgressTracker
        currentAgent={currentAgent}
        completedAgents={completedAgents}
        progressPercent={progressPercent}
      />
      <p className="mt-10 text-gray-500 text-sm">
        This usually takes 30–90 seconds depending on repo size.
      </p>
    </div>
  );
}
