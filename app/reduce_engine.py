# pyrefly: ignore [missing-import]
from rapidfuzz import fuzz
from typing import List, Dict, Any
from .models import ActionItemCandidate, FinalActionItem, Phase2Output, Phase3Output
import re
import uuid

class ReduceEngine:
    def __init__(self):
        self.similarity_threshold = 85.0

    def _normalize(self, text: str) -> str:
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def flatten(self, phase2_output: Phase2Output) -> List[ActionItemCandidate]:
        items = []
        for result in phase2_output.raw_results:
            items.extend(result.items)
        return items

    def group_duplicates(self, items: List[ActionItemCandidate]) -> List[List[ActionItemCandidate]]:
        groups = []
        used_indices = set()
        
        for i, item in enumerate(items):
            if i in used_indices:
                continue
            
            current_group = [item]
            used_indices.add(i)
            
            norm_title_i = self._normalize(item.title)
            
            for j, other_item in enumerate(items):
                if j in used_indices:
                    continue
                
                norm_title_j = self._normalize(other_item.title)
                
                similarity = fuzz.ratio(norm_title_i, norm_title_j)
                if similarity >= self.similarity_threshold:
                    current_group.append(other_item)
                    used_indices.add(j)
            
            groups.append(current_group)
            
        return groups

    def _merge_group(self, group: List[ActionItemCandidate], action_index: int) -> FinalActionItem:
        best_title = group[0].title
        best_desc = group[0].description
        
        assignees = [i.assignee for i in group if i.assignee.strip()]
        best_assignee = assignees[0] if assignees else ""
        
        deadlines = [i.due_context for i in group if i.due_context.strip()]
        best_due = deadlines[0] if deadlines else ""
        
        priorities = [i.priority for i in group if i.priority.strip()]
        if priorities:
            best_priority = max(set(priorities), key=priorities.count)
        else:
            best_priority = ""
            
        avg_confidence = round(sum(i.confidence for i in group) / len(group), 2)
        
        source_chunks = sorted(list(set([i.chunk_id for i in group])))
        
        action_id = f"ACT-{action_index:03d}"
        
        return FinalActionItem(
            action_id=action_id,
            title=best_title,
            description=best_desc,
            assignee=best_assignee,
            priority=best_priority,
            due_context=best_due,
            confidence=avg_confidence,
            source_chunks=source_chunks
        )

    def process(self, phase2_output: Phase2Output, transcript_id: str = "") -> Phase3Output:
        if not transcript_id:
            transcript_id = f"TR-{uuid.uuid4().hex[:6].upper()}"
            
        items = self.flatten(phase2_output)
        groups = self.group_duplicates(items)
        
        final_actions = []
        for idx, group in enumerate(groups, start=1):
            merged = self._merge_group(group, idx)
            final_actions.append(merged)
            
        return Phase3Output(
            transcript_id=transcript_id,
            total_chunks=phase2_output.processed_chunks,
            total_raw_items=len(items),
            final_action_items=len(final_actions),
            actions=final_actions
        )
