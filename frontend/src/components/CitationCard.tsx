"use client";
import { useState } from 'react';
import { ChevronDown, ChevronUp, FileText } from 'lucide-react';

interface CitationProps {
  page_number: number;
  section_title: string;
  text_preview: string;
}

export default function CitationCard({ citation }: { citation: CitationProps }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="mt-2 mb-3 bg-[#1e222b] border border-[rgba(255,255,255,0.05)] rounded-lg overflow-hidden transition-all duration-200">
      <button 
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-3 hover:bg-[rgba(255,255,255,0.02)] transition-colors"
      >
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4 text-blue-400" />
          <span className="text-sm font-medium text-gray-200 text-left">
            Page {citation.page_number} - {citation.section_title}
          </span>
        </div>
        {expanded ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
      </button>
      
      {expanded && (
        <div className="p-4 pt-1 bg-[#171a21] border-t border-[rgba(255,255,255,0.02)]">
          <p className="text-xs text-gray-400 leading-relaxed font-mono">
            "{citation.text_preview}..."
          </p>
        </div>
      )}
    </div>
  );
}
