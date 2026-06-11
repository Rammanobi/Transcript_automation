# Phase 3
PHASE 3 — REDUCE ENGINE, VALIDATION ENGINE, DEDUPLICATION ENGINE, FINAL OUTPUT GENERATION

PROJECT OBJECTIVE

Transform raw chunk-level action item candidates into a single clean, validated, production-ready action item list.

This phase receives all outputs from the Map phase.

This phase is responsible for:

* Merging duplicate action items
* Consolidating ownership
* Filling missing information
* Ranking confidence
* Removing invalid tasks
* Producing final structured JSON

This phase ends when a final validated action-item list is generated and ready to be sent to n8n.

No Jira creation.

No Slack messaging.

Only final action-item generation.

==================================================
INPUT TO PHASE 3
================

Input arrives from Map Phase.

Example:

{
"processed_chunks": 6,
"raw_results": [
{
"chunk_id": 1,
"items": [...]
},
{
"chunk_id": 2,
"items": [...]
}
]
}

Each chunk contains independently extracted action items.

==================================================
WHY REDUCE EXISTS
=================

Because overlap creates duplicates.

Example:

Chunk 1:

"Sarah should update landing page."

Chunk 2:

"Sarah should update landing page before Friday."

Both chunks detect:

Update Landing Page

Result:

Duplicate tasks.

Reduce must consolidate them.

==================================================
REDUCE PIPELINE
===============

Raw Results
↓
Flatten Results
↓
Normalize Text
↓
Group Similar Tasks
↓
Merge Duplicates
↓
Resolve Ownership
↓
Resolve Deadlines
↓
Resolve Priority
↓
Confidence Aggregation
↓
Validation
↓
Final JSON

==================================================
STEP 1
FLATTEN RAW RESULTS
===================

Input:

[
{
"chunk_id":1,
"items":[...]
},
{
"chunk_id":2,
"items":[...]
}
]

Convert into:

[
item1,
item2,
item3,
item4
]

Single list.

Purpose:

Simplify downstream processing.

==================================================
STEP 2
NORMALIZATION
=============

Before duplicate detection:

Normalize text.

Examples:

"Update Landing Page"

"Update the Landing Page"

"Landing Page Update"

Should become comparable.

Normalization Rules:

1. Lowercase

2. Trim spaces

3. Remove duplicate whitespace

4. Standardize punctuation

5. Remove formatting artifacts

==================================================
STEP 3
DUPLICATE DETECTION
===================

Goal:

Identify semantically identical tasks.

Example:

Task A

"Update Landing Page"

Task B

"Update landing page"

Task C

"Sarah should update landing page"

These represent one action.

==================================================
IMPORTANT DECISION
==================

Do NOT use embeddings.

Reason:

Dataset is tiny.

Usually:

5-30 action items.

Simple similarity comparison is sufficient.

Use:

RapidFuzz

Package:

pip install rapidfuzz

==================================================
SIMILARITY THRESHOLD
====================

Recommended:

85%

Example:

"Update Landing Page"

"Update Landing Page Before Friday"

Similarity:

92%

Merge.

Example:

"Update Landing Page"

"Review Pricing Structure"

Similarity:

12%

Keep separate.

==================================================
TASK GROUPING
=============

Example:

Group A

Task 1
Task 3
Task 8

Group B

Task 2
Task 5

Group C

Task 4

Each group becomes one candidate task.

==================================================
STEP 4
MERGE DUPLICATES
================

After grouping:

Create one master record.

Example:

Group:

Task A

{
"title":"Update Landing Page",
"assignee":"Sarah"
}

Task B

{
"title":"Update Landing Page Before Friday",
"due_context":"Friday"
}

Merged Result:

{
"title":"Update Landing Page",
"assignee":"Sarah",
"due_context":"Friday"
}

==================================================
STEP 5
OWNERSHIP RESOLUTION
====================

Example:

Chunk 1:

Assignee:
Sarah

Chunk 2:

Assignee:
Unknown

Choose:

Sarah

Rule:

Known owner beats unknown owner.

==================================================
OWNERSHIP PRIORITY
==================

1. Explicit owner

Example:

"Sarah will handle this"

Highest confidence.

2. Mentioned owner

Example:

"Sarah probably should handle this"

Medium confidence.

3. Unknown

Lowest confidence.

==================================================
STEP 6
DEADLINE RESOLUTION
===================

Example:

Chunk 1

Deadline:
Friday

Chunk 2

Deadline:
Not Found

Keep:

Friday

Rule:

Specific date wins.

==================================================
DEADLINE PRIORITY
=================

Specific Date

↓

Relative Date

↓

No Date

==================================================
STEP 7
PRIORITY RESOLUTION
===================

Map Phase may produce:

High

Medium

Low

Multiple chunks may disagree.

==================================================
PRIORITY VOTING
===============

Example:

Chunk 1

High

Chunk 2

High

Chunk 3

Medium

Final:

High

Majority wins.

==================================================
STEP 8
CONFIDENCE AGGREGATION
======================

Map Phase outputs:

0.91

0.88

0.95

Same task.

Aggregate:

Average:

0.913

Store:

0.91

==================================================
CONFIDENCE MEANING
==================

0.90+

Very Strong

0.75-0.89

Strong

0.60-0.74

Medium

Below 0.60

Weak

==================================================
STEP 9
VALIDATION ENGINE
=================

Before final output:

Every action item must pass validation.

==================================================
VALIDATION RULES
================

Rule 1

Must have title.

Rule 2

Title cannot be empty.

Rule 3

Title must be actionable.

Bad:

"Landing Page"

Good:

"Update Landing Page"

Rule 4

Description must exist.

Rule 5

Duplicate IDs removed.

==================================================
OPTIONAL LLM VALIDATION PASS
============================

Recommended.

Send merged results to Gemini.

Prompt:

Review these action items.

Remove duplicates.

Improve wording.

Fill obvious gaps.

Return JSON only.

This acts as final quality gate.

==================================================
WHY THIS HELPS
==============

Map Phase:

Local understanding.

Reduce Phase:

Global understanding.

LLM Validator:

Human-like review.

Together:

Much higher quality.

==================================================
FINAL OUTPUT FORMAT
===================

[
{
"action_id":"ACT-001",
"title":"Update Landing Page",
"description":"Update homepage content and design.",
"assignee":"Sarah",
"priority":"High",
"due_context":"Friday",
"confidence":0.91,
"source_chunks":[1,2,3]
}
]

==================================================
ACTION ID GENERATION
====================

Generate:

ACT-001
ACT-002
ACT-003

Purpose:

Tracking

Debugging

Future Jira Mapping

==================================================
SOURCE CHUNKS
=============

Preserve provenance.

Example:

"source_chunks":[1,2,3]

Allows debugging.

Shows where action came from.

==================================================
FINAL OUTPUT OBJECT
===================

{
"transcript_id":"TR-001",
"total_chunks":6,
"total_raw_items":22,
"final_action_items":8,
"actions":[...]
}

==================================================
WEBHOOK OUTPUT
==============

This exact object becomes:

POST

to

n8n webhook

No transformation required.

n8n receives clean validated action items.

==================================================
COMPLETE SYSTEM FLOW
====================

PDF / DOCX / TEXT
↓
Extraction
↓
Cleaning
↓
RecursiveCharacterTextSplitter
↓
Dynamic Chunks
↓
Map Phase
↓
Chunk Action Items
↓
Reduce Engine
↓
Deduplication
↓
Merge
↓
Validation
↓
Confidence Ranking
↓
Final JSON
↓
n8n Webhook

==================================================
SUCCESS CRITERIA
================

Phase 3 is complete when:

1. Duplicate tasks are merged.
2. Owners are resolved.
3. Deadlines are resolved.
4. Priorities are resolved.
5. Confidence scores calculated.
6. Validation passes.
7. Action IDs generated.
8. Source chunks preserved.
9. Final JSON generated.
10. JSON ready for n8n webhook.

END OF PHASE 3
