import UrlInput from "../components/UrlInput";

export default function Home({ onSubmit, loading }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] px-4">
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-white mb-3">
          Codebase Onboarding Agent
        </h1>
        <p className="text-gray-400 text-lg max-w-xl">
          Paste a public GitHub repo URL and get a comprehensive onboarding guide
          for new developers — powered by AI agents.
        </p>
      </div>
      <UrlInput onSubmit={onSubmit} loading={loading} />
    </div>
  );
}
