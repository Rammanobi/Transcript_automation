import type { Phase3Output } from '../types/actionItem';

export interface JobStatus {
  job_id: string;
  status: string;
  error?: string | null;
}

export interface JobResultResponse {
  status: string;
  webhook_status: string;
  results: Phase3Output;
}

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export async function analyzeTranscript(text?: string, file?: File): Promise<{ job_id: string; status: string }> {
  const formData = new FormData();
  if (file) {
    formData.append('file', file);
  } else if (text) {
    formData.append('text', text);
  } else {
    throw new Error("Must provide text or file.");
  }

  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to start analysis');
  }

  return await response.json();
}

export async function getJobStatus(jobId: string): Promise<JobStatus> {
  const response = await fetch(`${API_BASE_URL}/status/${jobId}`);
  if (!response.ok) {
    throw new Error('Failed to get job status');
  }
  return await response.json();
}

export async function getJobResults(jobId: string): Promise<JobResultResponse> {
  const response = await fetch(`${API_BASE_URL}/results/${jobId}`);
  if (!response.ok) {
    throw new Error('Failed to get job results');
  }
  return await response.json();
}
