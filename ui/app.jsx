// ui/app.jsx – Landing page for Render deployment

import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ArrowRight } from "lucide-react";
import { motion } from "framer-motion";

export default function LandingPage() {
  const handleCTA = () => {
    window.location.href = "https://cloudocs-ai-agent-1.onrender.com/ask";
  };

  return (
    <main className="min-h-screen bg-white text-gray-900 font-sans">
      <header className="flex justify-between items-center px-6 py-4 shadow-sm border-b">
        <div className="flex items-center gap-2">
          <img src="/logo.png" alt="CloudDocs Logo" className="w-8 h-8" />
          <span className="text-xl font-semibold text-blue-800">CloudDocs AI</span>
        </div>
      </header>

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
          <Button size="lg" className="rounded-2xl text-lg px-6" onClick={handleCTA}>
            Start Asking Questions <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </section>

      <section className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto px-6 py-16">
        {["Powered by real-time Microsoft Docs", "No hallucinations, only trusted content", "Deep coverage of Azure, Key Vault, AI Services, and more", "Designed for developers, architects, and cloud teams"].map((text, i) => (
          <Card key={i} className="shadow-md">
            <CardContent className="p-6 text-left text-base font-medium text-gray-800">
              {text}
            </CardContent>
          </Card>
        ))}
      </section>
    </main>
  );
}
