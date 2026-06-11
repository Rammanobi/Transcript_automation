export interface ActionItem {
  action_id: string;
  title: string;
  description: string;
  assignee: string;
  priority: string;
  due_context: string;
  confidence: number;
  source_chunks: number[];
}

export interface Phase3Output {
  transcript_id: string;
  total_chunks: number;
  total_raw_items: number;
  final_action_items: number;
  actions: ActionItem[];
}
