# Phase 2
PHASE 2 — MAP PROCESSING ENGINE

PROJECT OBJECTIVE

Convert transcript chunks into structured action-item candidates using a Map-Reduce architecture.

This phase is responsible for:

* LLM communication
* Chunk processing
* Action item extraction
* Retry handling
* Rate limiting protection
* Partial result collection

This phase DOES NOT include:

* Reduce
* Jira
* Slack
* Final validation

Those belong to later phases.

==================================================
INPUT TO PHASE 2
================

Output from Phase 1:

{
"transcript_length": 2200,
"chunk_count": 6,
"chunks": [
{
"chunk_id": 1,
"content": "..."
},
{
"chunk_id": 2,
"content": "..."
}
]
}

==================================================
PHASE 2 GOAL
============

Each chunk should be independently analyzed.

Each chunk produces:

* Action items
* Owners
* Deadlines
* Priority indicators
* Supporting context

Output should be structured JSON.

==================================================
MAP REDUCE THEORY
=================

Map Phase:

Chunk 1
→ Extract Action Items

Chunk 2
→ Extract Action Items

Chunk 3
→ Extract Action Items

Chunk N
→ Extract Action Items

Each chunk works independently.

No chunk knows about any other chunk.

==================================================
ARCHITECTURE
============

Chunk List
↓
Map Controller
↓
Chunk Queue
↓
LLM Calls
↓
Chunk Results
↓
Partial Action Item Collection

==================================================
FLOW
====

Chunk 1
↓
LLM

Chunk 2
↓
LLM

Chunk 3
↓
LLM

Chunk 4
↓
LLM

Chunk N
↓
LLM

All outputs collected.

==================================================
LLM CHOICE
==========

Primary:

Gemini

Architecture must remain provider-agnostic.

Future replacement should require minimal code changes.

Supported Future Models:

* Gemini
* Claude
* GPT
* DeepSeek

Create a Provider Layer.

Example:

llm_service.py

Responsibilities:

* Send prompts
* Handle retries
* Parse responses
* Normalize outputs

Application should never call Gemini directly from business logic.

==================================================
MAP PHASE PROMPT DESIGN
=======================

Prompt Objective:

Extract ALL action items.

Prompt Requirements:

1. Explicit action items.

Example:

"John will update the landing page."

2. Implicit action items.

Example:

"We should review the pricing structure."

3. Follow-ups.

4. Deadlines.

5. Ownership.

6. Dependencies.

7. Context.

==================================================
MAP PHASE OUTPUT FORMAT
=======================

Each chunk must return:

[
{
"title": "",
"description": "",
"assignee": "",
"priority": "",
"due_context": "",
"chunk_id": 1,
"confidence": ""
}
]

Nothing else.

No markdown.

No explanation.

Only JSON.

==================================================
CONFIDENCE SCORE
================

Required.

Example:

{
"confidence": 0.92
}

Purpose:

Later Reduce stage can prioritize stronger evidence.

==================================================
CHUNK METADATA
==============

Each result must preserve:

{
"chunk_id": 3
}

Reason:

Later debugging.

Example:

Action Item #17

Originated from:

Chunk 4

Easy traceability.

==================================================
PROCESSING STRATEGY
===================

Do NOT process all chunks simultaneously.

Do NOT process one chunk at a time.

Use Hybrid Processing.

==================================================
HYBRID EXECUTION MODEL
======================

Recommended:

2 concurrent requests.

Example:

Wave 1

Chunk 1
Chunk 2

Parallel

Wait

Wave 2

Chunk 3
Chunk 4

Parallel

Wait

Wave 3

Chunk 5
Chunk 6

Parallel

Benefits:

* Lower latency
* Safer rate limits
* Easier debugging

==================================================
WHY NOT FULL PARALLEL
=====================

Example:

100 chunks

Full Parallel:

100 API Calls

Problems:

* Rate limiting
* API throttling
* Cost spikes
* Hard debugging

Hybrid execution is safer.

==================================================
RATE LIMITING STRATEGY
======================

Every API call must include:

Try
Catch
Retry

==================================================
EXPONENTIAL BACKOFF
===================

Attempt 1

Immediate

Fail

Wait 1 second

Attempt 2

Fail

Wait 2 seconds

Attempt 3

Fail

Wait 4 seconds

Attempt 4

Fail

Wait 8 seconds

Attempt 5

Fail

Abort

==================================================
MAX RETRIES
===========

Recommended:

5 retries

After 5 failures:

Mark chunk as failed.

Continue workflow.

Never crash entire transcript.

==================================================
PARTIAL FAILURE STRATEGY
========================

Example:

Chunk 1
Success

Chunk 2
Success

Chunk 3
Failed

Chunk 4
Success

Chunk 5
Success

Workflow continues.

Failed chunks logged.

System remains operational.

==================================================
LOGGING REQUIREMENTS
====================

Log:

Chunk ID

Start Time

End Time

Duration

Token Usage

Model Used

Retry Count

Success / Failure

==================================================
RESULT COLLECTION
=================

After each chunk completes:

Store result.

Example:

[
{
"chunk_id": 1,
"items": [...]
},
{
"chunk_id": 2,
"items": [...]
}
]

These are RAW results.

Not validated.

Not deduplicated.

==================================================
PHASE 2 OUTPUT
==============

Final Output:

{
"processed_chunks": 6,
"successful_chunks": 6,
"failed_chunks": 0,
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

==================================================
SUCCESS CRITERIA
================

Phase 2 is complete when:

1. Dynamic chunks enter Map engine.
2. LLM processes chunks.
3. Two-concurrent execution works.
4. Retry system works.
5. Exponential backoff works.
6. Failed chunks do not crash workflow.
7. JSON responses are validated.
8. Raw results are collected.
9. Chunk metadata preserved.
10. Output is ready for Reduce stage.

END OF PHASE 2
