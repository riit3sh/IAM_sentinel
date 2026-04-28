"use client";
import { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Loader2, ShieldCheck, AlertCircle } from 'lucide-react';
import CitationCard from './CitationCard';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: any[];
  retries?: number;
}

export default function ChatPanel({ onNewQuery }: { onNewQuery: (query: string) => void }) {
  const [messages, setMessages] = useState<Message[]>([{
    role: 'assistant',
    content: 'Hello. I am the AWS IAM Sentinel. I am strictly grounded in the official AWS IAM User Guide. Ask me anything about IAM policies, MFA, or security best practices.'
  }]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const preMadeQuestions = [
    "How do I securely configure cross-account roles?",
    "What is the best practice for root account MFA?",
    "How can I set up an IAM permissions boundary?",
    "Explain the principle of least privilege in IAM."
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const sendQuery = async (queryText: string) => {
    if (!queryText.trim() || isLoading) return;

    const userMsg = queryText.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setIsLoading(true);
    onNewQuery(userMsg);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/api/v1/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg })
      });
      
      if (!res.ok) throw new Error('API Error');
      const data = await res.json();
      
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.response,
        citations: data.citations,
        retries: data.retries_used
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'I encountered an error connecting to the backend. Please ensure the FastAPI server is running, and that you have entered your API Key in the .env.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendQuery(input);
  };

  return (
    <div className="flex-1 flex flex-col h-screen bg-[#0f1115] relative">
      {/* Header */}
      <div className="h-16 border-b border-[rgba(255,255,255,0.08)] glass-panel flex items-center justify-between px-6 z-10 sticky top-0">
        <h2 className="font-semibold text-gray-200">Security Audit Chat</h2>
        <div className="flex items-center gap-2 text-xs font-medium text-emerald-400 bg-emerald-400/10 px-3 py-1.5 rounded-full border border-emerald-400/20">
          <ShieldCheck className="w-4 h-4" />
          Grounded mode active
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-4 max-w-4xl mx-auto animate-fade-in ${msg.role === 'assistant' ? '' : 'flex-row-reverse'}`}>
            <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${msg.role === 'assistant' ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30' : 'bg-gray-700 text-gray-300'}`}>
              {msg.role === 'assistant' ? <Bot className="w-5 h-5" /> : <User className="w-5 h-5" />}
            </div>
            
            <div className={`flex flex-col gap-2 max-w-[85%] ${msg.role === 'user' ? 'items-end' : ''}`}>
              <div className={`p-4 rounded-2xl leading-relaxed text-sm shadow-sm ${msg.role === 'user' ? 'bg-blue-600 text-white rounded-tr-none' : 'glass-panel text-gray-200 rounded-tl-none whitespace-pre-wrap'}`}>
                {msg.content}
              </div>
              
              {/* Hallucination Retry Warning */}
              {msg.retries && msg.retries > 0 ? (
                <div className="flex items-center gap-1.5 text-amber-400/80 text-xs mt-1 px-1">
                  <AlertCircle className="w-3.5 h-3.5" />
                  Self-reflection caught hallucination. Rewrote {msg.retries} {msg.retries === 1 ? 'time' : 'times'}.
                </div>
              ) : null}

              {/* Citations */}
              {msg.citations && msg.citations.length > 0 && (
                <div className="mt-2 w-full">
                  <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2 px-1">Retrieved Sources</h4>
                  <div className="flex flex-col gap-1">
                    {msg.citations.map((cite, i) => (
                      <CitationCard key={i} citation={cite} />
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
        
        {messages.length === 1 && (
          <div className="max-w-4xl mx-auto mt-8 grid grid-cols-1 md:grid-cols-2 gap-4 animate-fade-in px-4">
            {preMadeQuestions.map((q, i) => (
              <button 
                key={i}
                onClick={() => sendQuery(q)}
                className="text-left p-4 glass-panel hover:bg-[rgba(255,255,255,0.05)] border border-[rgba(255,255,255,0.05)] rounded-xl text-sm text-gray-300 hover:text-white transition-all cursor-pointer shadow-sm hover:shadow-md"
              >
                {q}
              </button>
            ))}
          </div>
        )}

        {isLoading && (
          <div className="flex gap-4 max-w-4xl mx-auto animate-fade-in">
            <div className="w-8 h-8 rounded-lg bg-blue-600/20 text-blue-400 border border-blue-500/30 flex items-center justify-center shrink-0">
              <Bot className="w-5 h-5" />
            </div>
            <div className="glass-panel p-4 rounded-2xl rounded-tl-none flex items-center gap-3">
              <Loader2 className="w-4 h-4 animate-spin text-blue-400" />
              <span className="text-sm text-gray-400">Analyzing AWS IAM Guide...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} className="h-4" />
      </div>

      {/* Input Area */}
      <div className="p-4 sm:p-6 bg-gradient-to-t from-[#0f1115] to-transparent">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about AWS IAM policies, security, MFA..."
            className="w-full glass-panel bg-[rgba(255,255,255,0.02)] border border-[rgba(255,255,255,0.1)] text-white placeholder-gray-500 rounded-xl pl-4 pr-12 py-4 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all shadow-xl"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-md cursor-pointer"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
        <p className="text-center text-[10px] text-gray-600 mt-3 font-medium">
          Powered by LangGraph & Qdrant. Grounded strictly in AWS IAM Documentation.
        </p>
      </div>
    </div>
  );
}
