"use client";
import { useState } from 'react';
import Sidebar from '@/components/Sidebar';
import ChatPanel from '@/components/ChatPanel';

export default function Home() {
  const [queries, setQueries] = useState<string[]>([]);

  const handleNewQuery = (query: string) => {
    setQueries(prev => [query, ...prev]);
  };

  return (
    <main className="flex h-screen w-full bg-[#0f1115] text-white overflow-hidden selection:bg-blue-500/30">
      <Sidebar queries={queries} />
      <ChatPanel onNewQuery={handleNewQuery} />
    </main>
  );
}
