import { useState } from 'react';

export default function JsonViewer({ data }: { data: any }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="mt-6 border border-gray-200 rounded shadow-sm overflow-hidden bg-white">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="w-full bg-gray-50 p-4 text-left font-semibold text-gray-700 flex justify-between items-center hover:bg-gray-100 transition-colors"
      >
        View Raw JSON
        <span className="text-gray-400">{isOpen ? '▲' : '▼'}</span>
      </button>
      {isOpen && (
        <pre className="bg-gray-900 text-green-400 p-4 overflow-x-auto text-xs font-mono">
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
    </div>
  );
}
