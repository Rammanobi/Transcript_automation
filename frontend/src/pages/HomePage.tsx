import { useState, useEffect } from 'react';
import TranscriptInput from '../components/TranscriptInput';
import TranscriptStats from '../components/TranscriptStats';
import ProcessingStatus from '../components/ProcessingStatus';
import ActionItemsTable from '../components/ActionItemsTable';
import JsonViewer from '../components/JsonViewer';
import { analyzeTranscript, getJobStatus, getJobResults } from '../services/api';
import type { Phase3Output } from '../types/actionItem';

export default function HomePage() {
  const [inputText, setInputText] = useState<string>();
  const [inputFile, setInputFile] = useState<File>();
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>('');
  const [results, setResults] = useState<Phase3Output | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [processingTime, setProcessingTime] = useState<number>(0);
  const [startTime, setStartTime] = useState<number | null>(null);

  const handleInputComplete = async (text?: string, file?: File) => {
    try {
      setInputText(text);
      setInputFile(file);
      setJobId(null);
      setStatus('');
      setResults(null);
      setError(null);
      setStartTime(Date.now());
      setProcessingTime(0);

      const res = await analyzeTranscript(text, file);
      setJobId(res.job_id);
      setStatus(res.status);
    } catch (err: any) {
      setError(err.message || "Failed to start analysis");
      setStatus("Failed");
    }
  };

  useEffect(() => {
    if (!jobId || status === 'Completed' || status === 'Failed') return;

    const interval = setInterval(async () => {
      try {
        const res = await getJobStatus(jobId);
        setStatus(res.status);
        if (res.error) {
          setError(res.error);
        }

        if (res.status === 'Completed') {
          const resultData = await getJobResults(jobId);
          setResults(resultData.results);
          if (startTime) {
            setProcessingTime(Date.now() - startTime);
          }
        }
      } catch (err: any) {
        console.error(err);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobId, status, startTime]);

  return (
    <div className="min-h-screen max-w-5xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight sm:text-4xl">
          Meeting Transcript Action Item Extractor
        </h1>
        <p className="mt-4 text-lg text-gray-500 max-w-2xl mx-auto">
          Upload a meeting transcript and extract action items using AI-powered Map-Reduce processing.
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6 rounded">
          <p className="text-sm text-red-700 font-medium">{error}</p>
        </div>
      )}

      <TranscriptInput 
        onInputComplete={handleInputComplete} 
        disabled={!!jobId && status !== 'Completed' && status !== 'Failed'} 
      />

      <TranscriptStats text={inputText} file={inputFile} />

      {jobId && <ProcessingStatus status={status} />}

      {results && status === 'Completed' && (
        <div className="mt-10 animate-fade-in-up">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white p-4 rounded shadow border border-gray-100 text-center">
              <div className="text-sm text-gray-500 uppercase tracking-wide font-semibold">Total Chunks</div>
              <div className="text-2xl font-bold text-gray-900 mt-1">{results.total_chunks}</div>
            </div>
            <div className="bg-white p-4 rounded shadow border border-gray-100 text-center">
              <div className="text-sm text-gray-500 uppercase tracking-wide font-semibold">Total Raw Items</div>
              <div className="text-2xl font-bold text-gray-900 mt-1">{results.total_raw_items}</div>
            </div>
            <div className="bg-white p-4 rounded shadow border border-gray-100 text-center">
              <div className="text-sm text-gray-500 uppercase tracking-wide font-semibold">Final Items</div>
              <div className="text-2xl font-bold text-blue-600 mt-1">{results.final_action_items}</div>
            </div>
            <div className="bg-white p-4 rounded shadow border border-gray-100 text-center">
              <div className="text-sm text-gray-500 uppercase tracking-wide font-semibold">Processing Time</div>
              <div className="text-2xl font-bold text-gray-900 mt-1">{(processingTime / 1000).toFixed(1)}s</div>
            </div>
          </div>

          <h2 className="text-2xl font-bold text-gray-900 mt-8 mb-4">Extracted Action Items</h2>
          <ActionItemsTable items={results.actions} />

          <JsonViewer data={results} />
        </div>
      )}
    </div>
  );
}
