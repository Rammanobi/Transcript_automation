

const STAGES = [
  "Transcript Loaded",
  "Transcript Cleaned",
  "Chunks Generated",
  "Map Processing",
  "Reduce Processing",
  "Generating Final Output",
  "Completed",
  "Failed"
];

export default function ProcessingStatus({ status }: { status: string }) {
  if (!status) return null;

  const currentIndex = STAGES.indexOf(status);

  return (
    <div className="bg-white p-6 rounded shadow mt-6 border border-gray-100">
      <h3 className="font-semibold text-gray-800 mb-4">Processing Progress</h3>
      <ul className="space-y-3">
        {STAGES.filter(s => s !== "Failed").map((stage, i) => {
          const isCompleted = currentIndex >= i && status !== "Failed";
          const isCurrent = status === stage;
          const isFailed = status === "Failed" && isCurrent;

          let icon = <span className="w-5 h-5 rounded-full border-2 border-gray-300 inline-block mr-3" />;
          if (isCompleted && !isCurrent) {
            icon = <span className="text-green-500 font-bold mr-3 text-lg leading-5">✓</span>;
          } else if (isCurrent && !isFailed && status !== "Completed") {
            icon = <span className="text-blue-500 font-bold mr-3 text-lg leading-5">⏳</span>;
          } else if (isCurrent && status === "Completed") {
            icon = <span className="text-green-500 font-bold mr-3 text-lg leading-5">✓</span>;
          } else if (isFailed) {
            icon = <span className="text-red-500 font-bold mr-3 text-lg leading-5">✗</span>;
          }

          return (
            <li key={stage} className={`flex items-center ${isCompleted || isCurrent ? 'text-gray-800' : 'text-gray-400'}`}>
              {icon}
              {stage}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
