import { useState } from 'react';

interface Props {
  onInputComplete: (text?: string, file?: File) => void;
  disabled: boolean;
}

export default function TranscriptInput({ onInputComplete, disabled }: Props) {
  const [method, setMethod] = useState<'paste' | 'upload'>('paste');
  const [text, setText] = useState('');
  const [file, setFile] = useState<File | null>(null);

  const handleSubmit = () => {
    if (method === 'paste' && text) {
      onInputComplete(text, undefined);
    } else if (method === 'upload' && file) {
      onInputComplete(undefined, file);
    }
  };

  const isReady = (method === 'paste' && text.length > 0) || (method === 'upload' && file !== null);

  return (
    <div className="bg-white p-6 rounded shadow border border-gray-100">
      <div className="flex gap-4 mb-4 border-b pb-2">
        {(['paste', 'upload'] as const).map(m => (
          <button
            key={m}
            className={`font-semibold pb-1 border-b-2 ${method === m ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'}`}
            onClick={() => { setMethod(m); setFile(null); setText(''); }}
            disabled={disabled}
          >
            {m === 'paste' ? 'Paste Transcript' : 'Upload File'}
          </button>
        ))}
      </div>
      
      {method === 'paste' && (
        <textarea
          className="w-full h-40 p-3 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
          placeholder="Paste meeting transcript here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={disabled}
        />
      )}
      
      {method === 'upload' && (
        <div className="border-2 border-dashed border-gray-300 rounded p-10 flex flex-col items-center justify-center">
          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            disabled={disabled}
            className="mb-2"
          />
          <p className="text-gray-500 text-sm">Accepts .pdf, .docx, and .txt files</p>
        </div>
      )}

      <div className="mt-4 flex justify-end">
        <button
          onClick={handleSubmit}
          disabled={disabled || !isReady}
          className="bg-blue-600 text-white px-6 py-2 rounded font-medium hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2 transition-all"
        >
          {disabled ? (
            <>
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processing...
            </>
          ) : (
            'Analyze Transcript'
          )}
        </button>
      </div>
    </div>
  );
}
