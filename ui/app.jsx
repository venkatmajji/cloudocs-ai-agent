// ui/app.jsx – Clean landing page for CloudDocs AI

import React from "react";
import { ArrowRight } from "lucide-react";
import { motion } from "framer-motion";

export default function LandingPage() {
  const handleCTA = () => {
    window.location.href = "https://cloudocs-ai-agent-6xv2.onrender.com/ask";
  };

  return (
    <main className="min-h-screen bg-white text-gray-900 font-sans">
      {/* Header */}
      <header className="flex justify-between items-center px-6 py-4 shadow-sm border-b">
        <div className="flex items-center gap-2">
          <img src="/logo.png" alt="CloudDocs Logo" className="w-8 h-8" />
          <span className="text-xl font-semibold text-blue-800">CloudDocs AI</span>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-24 px-6 text-center max-w-3xl mx-auto">
        <motion.h1
          className="text-4xl md:text-5xl font-bold mb-6"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          Your Smartest Way to Use Microsoft Docs
        </motion.h1>

        <p className="text-lg md:text-xl text-gray-600 mb-8">
          An AI agent built to understand, search, and answer questions directly from official Microsoft documentation — always accurate, always up to date.
        </p>

        <div className="flex justify-center">
          <button
            onClick={handleCTA}
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-2xl text-lg px-6 py-2 flex items-center transition"
          >
            Start Asking Questions <ArrowRight className="ml-2 h-5 w-5" />
          </button>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto px-6 py-16">
        {[
          "Powered by real-time Microsoft Docs",
          "No hallucinations, only trusted content",
          "Covers Azure, Key Vault, AI Services, and more",
          "Built for developers, architects, and cloud teams"
        ].map((text, i) => (
          <div
            key={i}
            className="rounded-xl border bg-white p-6 shadow-md text-left text-base font-medium text-gray-800"
          >
            {text}
          </div>
        ))}
      </section>
    </main>
  );
}
