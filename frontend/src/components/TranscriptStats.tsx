

interface Props {
  text?: string;
  file?: File;
}

export default function TranscriptStats({ text, file }: Props) {
  if (!text && !file) return null;

  let details = '';
  if (text) {
    const chars = text.length;
    const words = text.split(/\s+/).filter(Boolean).length;
    const chunks = Math.ceil(words / 400); // Rough estimate
    details = `Characters: ${chars} | Estimated Words: ${words} | Estimated Chunks: ${chunks}`;
  } else if (file) {
    details = `File: ${file.name} | Size: ${(file.size / 1024).toFixed(1)} KB`;
  }

  return (
    <div className="bg-white p-4 rounded shadow mt-6 border border-gray-100">
      <h3 className="font-semibold text-gray-700 mb-2">Input Statistics</h3>
      <p className="text-gray-600 text-sm font-mono">{details}</p>
    </div>
  );
}
