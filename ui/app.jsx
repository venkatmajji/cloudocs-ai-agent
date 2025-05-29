// ui/app.jsx – Enhanced UI with Tailwind styling and layout

import React, { useState } from "react";
import { ArrowRight } from "lucide-react";
import { motion } from "framer-motion";

export default function LandingPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setAnswer("");
    setSources([]);
    setError("");

    try {
      const res = await fetch("https://cloudocs-ai-agent-6xv2.onrender.com/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();

      if (data.error) {
        setError(data.error);
      } else {
        setAnswer(data.answer);
        setSources(data.sources || []);
      }
    } catch (err) {
      setError("Something went wrong. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-white text-gray-900 font-sans">
      <header className="flex justify-between items-center px-6 py-4 shadow-sm border-b bg-white sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <img src="/logo.png" alt="CloudDocs Logo" className="w-10 h-10 object-contain" />
          <span className="text-xl font-semibold text-blue-800">CloudDocs AI</span>
        </div>
      </header>

      <section className="py-16 px-6 text-center max-w-3xl mx-auto">
        <motion.h1
          className="text-4xl md:text-5xl font-bold mb-6"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          Your Smartest Way to Use Microsoft Docs
        </motion.h1>

        <p className="text-lg md:text-xl text-gray-600 mb-10">
          Ask questions about Azure, Key Vault, AI Services and more — directly powered by Microsoft documentation.
        </p>

        <form onSubmit={handleSubmit} className="w-full">
          <textarea
            className="w-full max-w-xl mx-auto border rounded-md p-4 text-base shadow-sm focus:ring-blue-500 resize-none"
            rows={4}
            placeholder="Ask something like: How does Azure Key Vault handle secrets?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            required
          />
          <button
            type="submit"
            disabled={loading}
            className="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl text-lg px-6 py-2 transition"
          >
            {loading ? "Thinking..." : "Get Answer"}
          </button>
        </form>

        {error && <p className="mt-4 text-red-600 font-medium">{error}</p>}

        {answer && (
          <div className="mt-10 text-left max-w-2xl mx-auto border rounded-md p-6 bg-gray-50">
            <h3 className="text-xl font-semibold text-blue-800 mb-2">Answer</h3>
            <p className="text-gray-800 whitespace-pre-wrap">{answer}</p>

            {sources.length > 0 && (
              <div className="mt-6">
                <h4 className="text-md font-semibold text-gray-700 mb-1">Sources:</h4>
                <ul className="list-disc list-inside text-sm text-blue-700">
                  {sources.map((src, i) => (
                    <li key={i}>
                      <a href={src.split("\n")[1]} target="_blank" rel="noopener noreferrer" className="underline">
                        {src.split("\n")[0]}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </section>
    </main>
  );
}
