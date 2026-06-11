import type { ActionItem } from '../types/actionItem';

export default function ActionItemsTable({ items }: { items: ActionItem[] }) {
  return (
    <div className="bg-white rounded shadow mt-6 overflow-hidden border border-gray-100">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm border-collapse">
          <thead>
            <tr className="bg-gray-50 text-gray-700 border-b">
              <th className="p-4 font-semibold">Action ID</th>
              <th className="p-4 font-semibold">Title</th>
              <th className="p-4 font-semibold">Assignee</th>
              <th className="p-4 font-semibold">Priority</th>
              <th className="p-4 font-semibold">Due</th>
              <th className="p-4 font-semibold">Confidence</th>
              <th className="p-4 font-semibold">Sources</th>
            </tr>
          </thead>
          <tbody>
            {items.map(item => (
              <tr key={item.action_id} className="border-b hover:bg-gray-50">
                <td className="p-4 font-mono text-gray-500 text-xs">{item.action_id}</td>
                <td className="p-4 font-medium text-gray-900 min-w-[200px]">
                  {item.title}
                  <div className="text-xs text-gray-500 mt-1 font-normal">{item.description}</div>
                </td>
                <td className="p-4 text-gray-700">{item.assignee || '-'}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${item.priority?.toLowerCase() === 'high' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700'}`}>
                    {item.priority || '-'}
                  </span>
                </td>
                <td className="p-4 text-gray-600">{item.due_context || '-'}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${item.confidence > 0.8 ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}`}>
                    {item.confidence?.toFixed(2)}
                  </span>
                </td>
                <td className="p-4 text-gray-500 text-xs text-center">
                  {item.source_chunks.join(', ')}
                </td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr>
                <td colSpan={7} className="p-8 text-center text-gray-500">
                  No action items found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
